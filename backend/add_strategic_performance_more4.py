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
    {"title": "Self-Leadership Training", "vimeo": "416673861"},
    {"title": "Self Appraisal (Purpose, Process & Steps)", "vimeo": "416677505"},
    {"title": "The Positive Effect of Self Appraisal", "vimeo": "416681576"},
    {"title": "Performance Management and Teams", "vimeo": "416687182"},
    {"title": "Basic Principles For Designing a PM System for Teams", "vimeo": "416683771"},
    {"title": "360 Degree Appraisal & what it Measures", "vimeo": "416689923"},
    {"title": "Considerations before Implementation", "vimeo": "416693307"},
    {"title": "Advantages and Issues in 360 Degree Appraisal", "vimeo": "416691034"},
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
            "order": 43 + i
        })
        print(f"  [{43+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {43 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
