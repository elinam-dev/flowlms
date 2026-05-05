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

LESSONS = [
    {"title": "Development Plans", "vimeo": "416699027"},
    {"title": "Development Plan Objectives & Examples", "vimeo": "416695513"},
    {"title": "Coaching (Performance Management Skills)", "vimeo": "416703126"},
    {"title": "Understanding Coaching (Definition, Benefits, Differences)", "vimeo": "416707040"},
    {"title": "Coaching Strategy (Performance Management & Coaching)", "vimeo": "416711955"},
    {"title": "Coaching to Improve Poor Performance", "vimeo": "416714458"},
    {"title": "Major Coaching Functions, Behaviours, Styles & Success Factors", "vimeo": "416717990"},
    {"title": "Coaching Process", "vimeo": "416821153"},
    {"title": "Organizational Activities to Improve Documentation of Performance", "vimeo": "416824158"},
]

def make_content(vimeo_id):
    return f'<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/{vimeo_id}?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def add():
    course = await db.courses.find_one(
        {'title': {'$regex': 'diploma in strategic performance', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_id = modules[0]['id']

    for i, lesson in enumerate(LESSONS):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": lesson["title"],
            "content_type": "embed",
            "content": make_content(lesson["vimeo"]),
            "duration_minutes": 10,
            "order": 56 + i
        })
        print(f"  [{56+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {56 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
