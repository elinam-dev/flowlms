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

async def check():
    # Find incoterms lesson
    lesson = await db.lessons.find_one({"content": {"$regex": "incoterms1"}})
    if lesson:
        print(f"Lesson: {lesson['title']}")
        print(f"Module ID: {lesson['module_id']}")
        
        # Find module
        module = await db.modules.find_one({"id": lesson['module_id']})
        if module:
            print(f"Module: {module['title']}")
            print(f"Course ID: {module['course_id']}")
            
            # Find course
            course = await db.courses.find_one({"id": module['course_id']})
            if course:
                print(f"Course: {course['title']}")

if __name__ == "__main__":
    asyncio.run(check())
