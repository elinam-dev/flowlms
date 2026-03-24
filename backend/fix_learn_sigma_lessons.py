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
    # Find the course
    course = await db.courses.find_one({"title": {"$regex": "Learn six sigma", "$options": "i"}})
    if not course:
        print("Course not found")
        return
    
    print(f"Found: {course['title']}")
    
    # Find or create module
    module = await db.modules.find_one({"course_id": course['id']})
    if not module:
        import uuid
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course['id'],
            "title": "Course Content",
            "order": 0
        })
        module = await db.modules.find_one({"id": module_id})
        print("Created module")
    
    # Update all learn_sigma_six lessons
    result = await db.lessons.update_many(
        {"content": {"$regex": "learn_sigma_six"}},
        {"$set": {"module_id": module['id']}}
    )
    
    print(f"Updated {result.modified_count} lessons")

if __name__ == "__main__":
    asyncio.run(fix())
