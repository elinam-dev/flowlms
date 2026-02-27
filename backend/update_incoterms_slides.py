import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def update_incoterms_lessons():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Get the Incoterms course
    course = await db.courses.find_one({"id": "incoterms_2024"})
    if not course:
        print("Incoterms course not found!")
        return
    
    # Get the module for this course
    module = await db.modules.find_one({"course_id": "incoterms_2024"})
    if not module:
        print("No module found, creating one...")
        import uuid
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": "incoterms_2024",
            "title": "Incoterms Overview",
            "description": "Complete guide to International Commercial Terms",
            "order": 0
        })
        module = await db.modules.find_one({"id": module_id})
    
    # Delete existing lessons
    await db.lessons.delete_many({"module_id": module["id"]})
    print(f"Deleted old lessons for module {module['id']}")
    
    # Create lessons for each image (86 images)
    base_url = "http://localhost:8000/uploads/images/incoterms"
    
    for i in range(1, 87):
        lesson_id = f"incoterms_lesson_{i}"
        image_url = f"{base_url}/incoterms{i}.jpeg"
        
        lesson_doc = {
            "id": lesson_id,
            "module_id": module["id"],
            "title": f"Slide {i}",
            "content_type": "image",
            "content": image_url,
            "duration_minutes": 2,
            "order": i - 1
        }
        
        await db.lessons.insert_one(lesson_doc)
    
    print(f"Created 86 image lessons for Incoterms course")
    
    # Verify
    lesson_count = await db.lessons.count_documents({"module_id": module["id"]})
    print(f"Total lessons in module: {lesson_count}")
    
    client.close()

if __name__ == '__main__':
    asyncio.run(update_incoterms_lessons())
