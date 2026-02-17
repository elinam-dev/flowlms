"""
Update Valve Presentation course with images
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def update_valve_course():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Find course
    course = await db.courses.find_one({"code": "ENG-VALVE-001"})
    if not course:
        print("Course not found, creating...")
        course_id = str(uuid.uuid4())
        await db.courses.insert_one({
            "id": course_id,
            "title": "Industrial Valves - Types and Applications",
            "description": "Complete guide to industrial valves including types, selection criteria, installation, and maintenance procedures.",
            "code": "ENG-VALVE-001",
            "category": "ENGINEERING",
            "course_type": "optional",
            "duration_hours": 2,
            "is_published": True,
            "thumbnail": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=400&h=225&fit=crop",
            "enrolled_users": [],
            "created_at": "2024-01-01T00:00:00"
        })
        course = await db.courses.find_one({"code": "ENG-VALVE-001"})
    
    # Find or create module
    module = await db.modules.find_one({"course_id": course['id']})
    if not module:
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course['id'],
            "title": "Course Content",
            "description": "Visual presentation for Industrial Valves",
            "order": 0
        })
        module = await db.modules.find_one({"course_id": course['id']})
    
    # Delete existing lessons
    await db.lessons.delete_many({"module_id": module['id']})
    
    # Create 18 lessons with images
    for i in range(1, 19):
        image_num = str(i).zfill(2)
        image_path = f"/api/uploads/documents/Valve Presentation/Valve Presentation_{image_num}.png"
        
        content = f'''<div class="lesson-content">
<div style="text-align: center; padding: 20px;">
<img src="{image_path}" alt="Slide {i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />
</div>
<div style="text-align: center; margin-top: 20px; color: #64748b;">
<p>Slide {i} of 18</p>
</div>
</div>'''
        
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module['id'],
            "title": f"Slide {i}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 5,
            "order": i - 1
        })
    
    # Create quiz if not exists
    quiz = await db.quizzes.find_one({"module_id": module['id']})
    if not quiz:
        await db.quizzes.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module['id'],
            "title": "Industrial Valves - Assessment",
            "description": "Test your understanding of Industrial Valves. Pass mark: 70%",
            "passing_score": 70,
            "questions": [
                {"question": "What is the primary function of a valve?", "type": "multiple_choice", "options": ["Control flow", "Generate pressure", "Filter fluid", "Measure flow"], "correct_answer": "Control flow"},
                {"question": "Gate valves are used for throttling.", "type": "true_false", "correct_answer": "false"},
                {"question": "What valve type is best for on/off service?", "type": "short_answer", "correct_answer": "Gate valve or ball valve"},
                {"question": "Which valve allows flow in one direction only?", "type": "multiple_choice", "options": ["Check valve", "Gate valve", "Globe valve", "Butterfly valve"], "correct_answer": "Check valve"},
                {"question": "What is Cv in valve sizing?", "type": "short_answer", "correct_answer": "Flow coefficient"},
                {"question": "Ball valves provide tight shutoff.", "type": "true_false", "correct_answer": "true"},
                {"question": "Which valve is best for throttling?", "type": "multiple_choice", "options": ["Globe valve", "Gate valve", "Check valve", "Plug valve"], "correct_answer": "Globe valve"},
                {"question": "Butterfly valves are quarter-turn valves.", "type": "true_false", "correct_answer": "true"},
                {"question": "What causes valve cavitation?", "type": "short_answer", "correct_answer": "High pressure drop"},
                {"question": "Which valve material resists corrosion best?", "type": "multiple_choice", "options": ["Stainless steel", "Cast iron", "Carbon steel", "Brass"], "correct_answer": "Stainless steel"}
            ],
            "time_limit_minutes": 20,
            "created_at": "2024-01-01T00:00:00"
        })
    
    print("OK Valve Presentation course updated with 18 slides")
    client.close()

if __name__ == "__main__":
    asyncio.run(update_valve_course())
