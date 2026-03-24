#!/usr/bin/env python3
"""
Delete non-embed lessons from the 'Course Content' module of
Diploma in Supply Chain Management, keeping all embed (video) lessons.
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

async def delete_old_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    if not course:
        print("Course not found!")
        return

    modules = await db.modules.find({"course_id": course["id"]}).to_list(None)
    course_content_module = next((m for m in modules if m["title"] == "Course Content"), None)

    if not course_content_module:
        print("'Course Content' module not found!")
        return

    lessons = await db.lessons.find({"module_id": course_content_module["id"]}).to_list(None)

    deleted = []
    kept = []
    for lesson in lessons:
        if lesson.get("content_type") == "embed":
            kept.append(lesson["title"])
        else:
            await db.lessons.delete_one({"id": lesson["id"]})
            deleted.append(lesson["title"])

    print(f"DELETED ({len(deleted)}):")
    for t in deleted:
        print(f"  - {t}")

    print(f"\nKEPT ({len(kept)}):")
    for t in kept:
        print(f"  + {t}")

if __name__ == "__main__":
    asyncio.run(delete_old_lessons())
