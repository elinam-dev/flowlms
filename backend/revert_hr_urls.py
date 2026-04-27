#!/usr/bin/env python3
"""Revert /uploads/images/hr/ back to /uploads/images/HR/ to match git paths"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def fix():
    # Fix lesson content
    lessons = await db.lessons.find({"content": {"$regex": "/uploads/images/hr/"}}).to_list(None)
    for lesson in lessons:
        new_content = lesson["content"].replace("/uploads/images/hr/", "/uploads/images/HR/")
        await db.lessons.update_one({"_id": lesson["_id"]}, {"$set": {"content": new_content}})
    print(f"Reverted {len(lessons)} lesson URLs back to /HR/")

    # Fix thumbnails
    courses = await db.courses.find({"thumbnail": {"$regex": "/uploads/images/hr/"}}).to_list(None)
    for course in courses:
        new_thumb = course["thumbnail"].replace("/uploads/images/hr/", "/uploads/images/HR/")
        await db.courses.update_one({"_id": course["_id"]}, {"$set": {"thumbnail": new_thumb}})
    print(f"Reverted {len(courses)} course thumbnails back to /HR/")

    print("Done!")

if __name__ == "__main__":
    asyncio.run(fix())
