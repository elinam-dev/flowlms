import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import uuid

load_dotenv('backend/.env')

async def recreate_incoterms_lessons():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Find Incoterms course
    incoterms_course = await db.courses.find_one({"title": {"$regex": "incoterms", "$options": "i"}})
    
    if not incoterms_course:
        print("No Incoterms course found")
        return
    
    # Get module
    modules = await db.modules.find({"course_id": incoterms_course["id"]}).to_list(100)
    if not modules:
        print("No modules found")
        return
    
    module_id = modules[0]["id"]
    
    # Delete existing lessons
    await db.lessons.delete_many({"module_id": module_id})
    
    # Create 86 lessons (one per slide)
    for i in range(1, 87):
        lesson_id = str(uuid.uuid4())
        slide_html = f'<div class="slide-container"><img src="/api/uploads/images/incoterms/incoterms{i}.jpeg" alt="Slide {i}" class="slide-image" /></div>'
        
        await db.lessons.insert_one({
            "id": lesson_id,
            "module_id": module_id,
            "title": f"Slide {i}",
            "content_type": "text",
            "content": slide_html,
            "duration_minutes": 2,
            "order": i - 1
        })
        
        print(f"Created lesson {i}: Slide {i}")
    
    print("Successfully created 86 individual slide lessons!")
    client.close()

if __name__ == "__main__":
    asyncio.run(recreate_incoterms_lessons())