#!/usr/bin/env python3
"""
Add all lessons to HRM - the ultimate employee onboarding guide with 4Cs and publish
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
    {"title": "Slide 1", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_001.jpeg"},
    {"title": "Slide 2", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_002.jpeg"},
    {"title": "Slide 3", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_003.jpeg"},
    {"title": "Slide 4", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_004.jpeg"},
    {"title": "Slide 5", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_005.jpeg"},
    {"title": "Slide 6", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_006.jpeg"},
    {"title": "Slide 7", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_007.jpeg"},
    {"title": "Slide 8", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_008.jpeg"},
    {"title": "Employee Onboarding Case Study", "type": "embed", "content": "https://player.vimeo.com/video/742086325?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Slide 9", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_009.jpeg"},
    {"title": "Checklist and Welcome Mail", "type": "embed", "content": "https://player.vimeo.com/video/742088871?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Slide 10", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_010.jpeg"},
    {"title": "Slide 11", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_011.jpeg"},
    {"title": "Slide 12", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_012.jpeg"},
    {"title": "Slide 13", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_013.jpeg"},
    {"title": "Slide 14", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_014.jpeg"},
    {"title": "Video 3: Case Study No.1", "type": "embed", "content": "https://player.vimeo.com/video/742090198?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Slide 15", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/HRM/hrm_015.jpeg"},
]

def make_content(lesson):
    if lesson["type"] == "image":
        return f'<div style="text-align: center; padding: 20px;"><img src="{lesson["content"]}" alt="{lesson["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
    else:
        return f'<div style="text-align: center;"><iframe src="{lesson["content"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def add_lessons():
    course = await db.courses.find_one(
        {"title": {"$regex": "ultimate employee onboarding", "$options": "i"}},
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
        print("Cleared existing lessons")

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

    await db.courses.update_one(
        {"id": course["id"]},
        {"$set": {"is_published": True}}
    )
    print(f"\nAdded {len(LESSONS)} lessons and published the course.")

if __name__ == "__main__":
    asyncio.run(add_lessons())
