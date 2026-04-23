#!/usr/bin/env python3
"""
Add lessons to Onboarding Principles for Employees course
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

BASE_URL = "https://flowlms-production.up.railway.app"

LESSONS = [
    {
        "title": "Onboarding Overview",
        "type": "image",
        "content": f"{BASE_URL}/uploads/images/HR/onboarding/onboarding01.jpeg"
    },
    {
        "title": "Purpose of Onboarding",
        "type": "embed",
        "content": "https://player.vimeo.com/video/887610175?quality=720p&audiotrack=main&texttrack=en"
    },
    {
        "title": "Introduction to Onboarding",
        "type": "embed",
        "content": "https://player.vimeo.com/video/887617641?quality=720p&audiotrack=main&texttrack=en"
    },
    {
        "title": "Onboarding Preparation",
        "type": "embed",
        "content": "https://player.vimeo.com/video/887617659?quality=720p&audiotrack=main&texttrack=en"
    },
]

def make_content(lesson):
    if lesson["type"] == "image":
        return f'<div style="text-align: center; padding: 20px;"><img src="{lesson["content"]}" alt="{lesson["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
    else:
        return f'<div style="text-align: center;"><iframe src="{lesson["content"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def add_lessons():
    course = await db.courses.find_one(
        {"title": {"$regex": "onboarding principles", "$options": "i"}},
        {"_id": 0}
    )
    if not course:
        print("Course not found!")
        return

    print(f"Found: {course['title']}")

    # Get or create module
    module = await db.modules.find_one({"course_id": course["id"]})
    if not module:
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course["id"],
            "title": "Course Content",
            "description": "Onboarding Principles for Employees",
            "order": 0
        })
        module = await db.modules.find_one({"id": module_id})
        print("Created module")
    else:
        await db.lessons.delete_many({"module_id": module["id"]})
        print(f"Cleared existing lessons")

    for i, lesson in enumerate(LESSONS):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson["title"],
            "content_type": "text" if lesson["type"] == "image" else "embed",
            "content": make_content(lesson),
            "duration_minutes": 5 if lesson["type"] == "image" else 10,
            "order": i
        })
        print(f"  [{i+1}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course NOT published yet — more lessons to come.")

if __name__ == "__main__":
    asyncio.run(add_lessons())
