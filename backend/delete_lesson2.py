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

async def delete_lesson():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"], "title": "Course Content"})
    
    lesson = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Supply Chain Networks"
    })
    
    if lesson:
        await db.lessons.delete_one({"id": lesson["id"]})
        print(f"Deleted: {lesson['title']}")
    else:
        print("Lesson not found!")

if __name__ == "__main__":
    asyncio.run(delete_lesson())
