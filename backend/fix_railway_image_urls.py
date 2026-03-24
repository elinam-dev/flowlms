#!/usr/bin/env python3
"""
Update all localhost:8000 image URLs in lessons and course thumbnails
to the Railway production URL.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

OLD = "http://localhost:8000"
NEW = "https://flowlms-production.up.railway.app"

async def update_urls():
    # Update lesson content
    lessons = await db.lessons.find({"content": {"$regex": OLD}}).to_list(None)
    lesson_count = 0
    for lesson in lessons:
        new_content = lesson["content"].replace(OLD, NEW)
        await db.lessons.update_one({"_id": lesson["_id"]}, {"$set": {"content": new_content}})
        lesson_count += 1
    print(f"Updated {lesson_count} lessons")

    # Update course thumbnails
    courses = await db.courses.find({"thumbnail": {"$regex": OLD}}).to_list(None)
    course_count = 0
    for course in courses:
        new_thumb = course["thumbnail"].replace(OLD, NEW)
        await db.courses.update_one({"_id": course["_id"]}, {"$set": {"thumbnail": new_thumb}})
        course_count += 1
    print(f"Updated {course_count} course thumbnails")

    print(f"\nDone! All localhost:8000 URLs replaced with Railway URL.")

if __name__ == "__main__":
    asyncio.run(update_urls())
