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
    {"title": "Module 5 Getting Started", "vimeo": "880336956"},
    {"title": "The History of Generational Gaps", "vimeo": "919756880"},
    {"title": "Case Study: The History of Generational Gaps", "vimeo": "925245613"},
    {"title": "The Legacy of Traditionalists: Understand the Shift", "vimeo": "919757571"},
    {"title": "Case Study: The Legacy of Traditionalists", "vimeo": "880337380"},
    {"title": "The Baby Boomer Generation", "vimeo": "880338882"},
    {"title": "Case Study: Baby Boomers", "vimeo": "880338949"},
    {"title": "Understanding Generation X", "vimeo": "880339007"},
    {"title": "Case Study: Generation X", "vimeo": "880339045"},
    {"title": "Understanding Generation Y", "vimeo": "880339081"},
    {"title": "Case Study: Generation Y", "vimeo": "880339796"},
    {"title": "Understanding Generation Z", "vimeo": "919759022"},
    {"title": "Generational Differences", "vimeo": "919759462"},
    {"title": "Case Study: Generational Differences", "vimeo": "880343484"},
    {"title": "Common Grounds", "vimeo": "880343547"},
    {"title": "Case Study: Common Grounds", "vimeo": "880343577"},
    {"title": "Conflict Management (I)", "vimeo": "880344761"},
]

def make_content(vimeo_id):
    return f'<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/{vimeo_id}?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def add():
    course = await db.courses.find_one(
        {'title': {'$regex': 'talent management and workforce', '$options': 'i'}},
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
            "order": 105 + i
        })
        print(f"  [{105+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {105 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
