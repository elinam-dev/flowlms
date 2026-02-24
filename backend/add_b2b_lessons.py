import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import uuid

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
BASE_URL = "https://flowlms-production.up.railway.app/api/uploads/images/B2B"

async def add_b2b_lessons():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": {"$regex": "Effective B2B communication", "$options": "i"}})
    
    if not course:
        print("Course not found")
        return
    
    print(f"Found course: {course['title']}")
    
    # Delete existing modules and lessons
    modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
    for module in modules:
        await db.lessons.delete_many({"module_id": module["id"]})
    await db.modules.delete_many({"course_id": course["id"]})
    
    # Create module
    module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": module_id,
        "course_id": course["id"],
        "title": "B2B Communication Fundamentals",
        "description": "Master effective B2B communication strategies",
        "order": 1
    })
    
    # Create 38 lessons
    for i in range(1, 39):
        lesson_id = str(uuid.uuid4())
        content = f'<div class="slide-content"><img src="{BASE_URL}/B2B{i}.jpeg" alt="B2B Slide {i}" style="width: 100%; max-width: 800px; height: auto; display: block; margin: 0 auto;" /></div>'
        
        await db.lessons.insert_one({
            "id": lesson_id,
            "module_id": module_id,
            "title": f"Slide {i}",
            "content": content,
            "order": i,
            "duration": 5
        })
    
    print(f"Added 38 lessons to B2B course")
    client.close()

if __name__ == "__main__":
    asyncio.run(add_b2b_lessons())
