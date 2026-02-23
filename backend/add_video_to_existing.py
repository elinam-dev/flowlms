import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import uuid

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Delete the duplicate I created
    dup = await db.courses.find_one({"code": "PB-MOT-001"})
    if dup:
        modules = await db.modules.find({"course_id": dup["id"]}).to_list(100)
        for module in modules:
            await db.lessons.delete_many({"module_id": module["id"]})
        await db.modules.delete_many({"course_id": dup["id"]})
        await db.quizzes.delete_many({"course_id": dup["id"]})
        await db.courses.delete_one({"id": dup["id"]})
        print("Deleted duplicate")
    
    # Find the existing course
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    if not course:
        print("Course not found")
        return
    
    # Check if it has modules
    modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
    
    if not modules:
        # Create module
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course["id"],
            "title": "Understanding Motivation",
            "description": "Learn about goals and what drives motivation",
            "order": 1
        })
        print("Created module")
    else:
        module_id = modules[0]["id"]
    
    # Add video lesson
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
    
    print("Added video lesson to existing course")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
