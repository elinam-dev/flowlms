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

async def fix():
    # Fix lesson content - emotional images were at /uploads/images/emotional
    lessons = await db.lessons.find({"content": {"$regex": "/uploads/images/emotional"}}).to_list(None)
    for lesson in lessons:
        new_content = lesson["content"].replace(
            "/uploads/images/emotional",
            "/uploads/images/personal_branding/emotional/emotional"
        )
        await db.lessons.update_one({"_id": lesson["_id"]}, {"$set": {"content": new_content}})
    print(f"Updated {len(lessons)} lesson URLs")

    # Fix thumbnail
    course = await db.courses.find_one({"thumbnail": {"$regex": "/uploads/images/emotional"}}, {"_id": 0, "id": 1, "thumbnail": 1})
    if course:
        new_thumb = course["thumbnail"].replace(
            "/uploads/images/emotional",
            "/uploads/images/personal_branding/emotional/emotional"
        )
        await db.courses.update_one({"id": course["id"]}, {"$set": {"thumbnail": new_thumb}})
        print("Updated course thumbnail")

    print("Done!")

if __name__ == "__main__":
    asyncio.run(fix())
