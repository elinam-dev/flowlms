#!/usr/bin/env python3
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

async def show_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    if not course:
        print("Course not found!")
        return
    
    modules = await db.modules.find({"course_id": course["id"]}).to_list(None)
    
    for module in modules:
        print(f"\nModule: {module['title']}")
        lessons = await db.lessons.find({"module_id": module["id"]}).to_list(None)
        
        for lesson in lessons:
            print(f"  - {lesson['title']}")
            print(f"    Type: {lesson.get('content_type', 'N/A')}")
            print(f"    ID: {lesson['id']}")

if __name__ == "__main__":
    asyncio.run(show_lessons())
