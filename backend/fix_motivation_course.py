import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Delete old course
    old_course = await db.courses.find_one({"code": "SOFT-MOT-001"})
    if old_course:
        course_id = old_course["id"]
        modules = await db.modules.find({"course_id": course_id}).to_list(100)
        for module in modules:
            await db.lessons.delete_many({"module_id": module["id"]})
        await db.modules.delete_many({"course_id": course_id})
        await db.quizzes.delete_many({"course_id": course_id})
        await db.courses.delete_one({"id": course_id})
        print("Deleted old course")
    
    # Create new course
    course_id = str(uuid.uuid4())
    module_id = str(uuid.uuid4())
    
    await db.courses.insert_one({
        "id": course_id,
        "title": "Motivation - Power Guide to Motivating Yourself and Others",
        "code": "PB-MOT-001",
        "description": "A comprehensive guide to understanding motivation and inspiring yourself and others to achieve greatness.",
        "category": "Personal Branding",
        "level": "Beginner",
        "duration": 30,
        "is_compulsory": False,
        "is_published": True,
        "thumbnail": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=400&h=225&fit=crop"
    })
    
    await db.modules.insert_one({
        "id": module_id,
        "course_id": course_id,
        "title": "Understanding Motivation",
        "description": "Learn about goals and what drives motivation",
        "order": 1
    })
    
    video_html = '''<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
    <iframe src="https://player.vimeo.com/video/346354555?quality=720p&audiotrack=main&texttrack=en" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
            frameborder="0" 
            allow="autoplay; fullscreen; picture-in-picture" 
            allowfullscreen>
    </iframe>
</div>'''
    
    await db.lessons.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module_id,
        "title": "Goals & What is Motivation",
        "content_type": "text",
        "content": video_html,
        "duration_minutes": 15,
        "order": 0
    })
    
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "course_id": course_id,
        "title": "Motivation Assessment",
        "passing_score": 70,
        "questions": [
            {
                "question": "What is the primary purpose of setting goals?",
                "type": "multiple_choice",
                "options": ["To impress others", "To provide direction and motivation", "To create stress", "To compete with others"],
                "correct_answer": "To provide direction and motivation"
            },
            {
                "question": "Intrinsic motivation comes from within yourself.",
                "type": "true_false",
                "correct_answer": "true"
            },
            {
                "question": "What type of goals are most effective?",
                "type": "multiple_choice",
                "options": ["Vague and general", "Specific and measurable", "Impossible to achieve", "Short-term only"],
                "correct_answer": "Specific and measurable"
            },
            {
                "question": "Motivation can be influenced by external rewards.",
                "type": "true_false",
                "correct_answer": "true"
            },
            {
                "question": "What does SMART stand for in goal setting?",
                "type": "short_answer",
                "correct_answer": "Specific Measurable Achievable Relevant Time-bound"
            }
        ]
    })
    
    print("Created new course: Motivation - Power Guide to Motivating Yourself and Others")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
