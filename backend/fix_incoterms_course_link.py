import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def fix():
    # Find the correct incoterms course
    course = await db.courses.find_one({"title": {"$regex": "incoterm", "$options": "i"}})
    if not course:
        print("No incoterms course found!")
        return
    
    print(f"Found course: {course['title']}")
    print(f"Course ID: {course['id']}")
    
    # Find or create module
    module = await db.modules.find_one({"course_id": course['id']})
    if not module:
        print("No module found, creating one...")
        import uuid
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course['id'],
            "title": "Incoterms Fundamentals",
            "description": "Learn about international commercial terms",
            "order": 0
        })
        module = await db.modules.find_one({"id": module_id})
    
    print(f"Module: {module['title']}, ID: {module['id']}")
    
    # Update all incoterms lessons to point to this module
    result = await db.lessons.update_many(
        {"content": {"$regex": "incoterms"}},
        {"$set": {"module_id": module['id']}}
    )
    
    print(f"Updated {result.modified_count} lessons")

if __name__ == "__main__":
    asyncio.run(fix())
