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

async def delete_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    modules = await db.modules.find({"course_id": course["id"]}).to_list(None)
    
    all_lessons = []
    for module in modules:
        lessons = await db.lessons.find({"module_id": module["id"]}).sort("order", 1).to_list(None)
        all_lessons.extend(lessons)
    
    # Delete from lesson 2 onwards (index 1+)
    deleted = 0
    for lesson in all_lessons[1:]:
        await db.lessons.delete_one({"id": lesson["id"]})
        print(f"Deleted: {lesson['title']}")
        deleted += 1
    
    print(f"\nTotal deleted: {deleted} lessons")

if __name__ == "__main__":
    asyncio.run(delete_lessons())
