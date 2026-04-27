#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE_URL = "https://flowlms-production.up.railway.app"

async def fix():
    # Fix lesson content URLs
    lessons = await db.lessons.find({"content": {"$regex": "/uploads/images/HR/"}}).to_list(None)
    for lesson in lessons:
        new_content = lesson["content"].replace("/uploads/images/HR/", "/uploads/images/hr/")
        await db.lessons.update_one({"_id": lesson["_id"]}, {"$set": {"content": new_content}})
    print(f"Updated {len(lessons)} lesson URLs")

    # Fix course thumbnails
    courses = await db.courses.find({"thumbnail": {"$regex": "/uploads/images/HR/"}}).to_list(None)
    for course in courses:
        new_thumb = course["thumbnail"].replace("/uploads/images/HR/", "/uploads/images/hr/")
        await db.courses.update_one({"_id": course["_id"]}, {"$set": {"thumbnail": new_thumb}})
    print(f"Updated {len(courses)} course thumbnails")

    print("Done!")

if __name__ == "__main__":
    asyncio.run(fix())
