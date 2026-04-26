#!/usr/bin/env python3
"""
Add embed lesson to Employee onboarding and motivation and publish
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def add_lessons():
    course = await db.courses.find_one(
        {"title": {"$regex": "employee onboarding and motivation", "$options": "i"}},
        {"_id": 0}
    )
    if not course:
        print("Course not found!")
        return
    print(f"Found: {course['title']}")

    module = await db.modules.find_one({"course_id": course["id"]})
    if not module:
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course["id"],
            "title": "Course Content",
            "order": 0
        })
        module = await db.modules.find_one({"id": module_id})
    else:
        await db.lessons.delete_many({"module_id": module["id"]})

    await db.lessons.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module["id"],
        "title": "Employee Onboarding and Motivation",
        "content_type": "embed",
        "content": '<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/1094800535?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>',
        "duration_minutes": 10,
        "order": 0
    })

    await db.courses.update_one(
        {"id": course["id"]},
        {"$set": {"is_published": True}}
    )
    print("Added 1 lesson and published the course.")

if __name__ == "__main__":
    asyncio.run(add_lessons())
