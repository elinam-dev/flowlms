#!/usr/bin/env python3
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
    # First batch of images (6)
    {"title": "Slide 23", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_023.jpeg"},
    {"title": "Slide 24", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_024.jpeg"},
    {"title": "Slide 25", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_025.jpeg"},
    {"title": "Slide 26", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_026.jpeg"},
    {"title": "Slide 27", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_027.jpeg"},
    {"title": "Slide 28", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_028.jpeg"},
    # Video
    {"title": "Case Study: Dealing with Onboarding Challenges", "type": "embed", "vimeo": "742094434"},
    # Last 7 images
    {"title": "Slide 29", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_029.jpeg"},
    {"title": "Slide 30", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_030.jpeg"},
    {"title": "Slide 31", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_031.jpeg"},
    {"title": "Slide 32", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_032.jpeg"},
    {"title": "Slide 33", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_033.jpeg"},
    {"title": "Slide 34", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_034.jpeg"},
    {"title": "Slide 35", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/HRM/hrm_035.jpeg"},
    # Final video
    {"title": "Case Study on Feedback Management", "type": "embed", "vimeo": "742095891"},
]

def make_content(lesson):
    if lesson["type"] == "image":
        return f'<div style="text-align: center; padding: 20px;"><img src="{lesson["url"]}" alt="{lesson["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
    else:
        return f'<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/{lesson["vimeo"]}?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def add():
    course = await db.courses.find_one(
        {'title': {'$regex': 'ultimate employee onboarding', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_id = modules[0]['id']

    for i, lesson in enumerate(LESSONS):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": lesson["title"],
            "content_type": "text" if lesson["type"] == "image" else "embed",
            "content": make_content(lesson),
            "duration_minutes": 5 if lesson["type"] == "image" else 10,
            "order": 26 + i
        })
        print(f"  [{26+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {26 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
