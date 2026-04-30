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
    {"title": "Case Study: Conflicts (I)", "type": "embed", "vimeo": "880344817"},
    {"title": "Conflict Management (II)", "type": "embed", "vimeo": "880344885"},
    {"title": "Case Study: Conflicts (II)", "type": "embed", "vimeo": "880344965"},
    {"title": "Power of the Four Generations", "type": "embed", "vimeo": "880345025"},
    {"title": "Case Study: Power of Generations", "type": "embed", "vimeo": "880345049"},
    {"title": "Module 5 Wrapping Up", "type": "embed", "vimeo": "880345079"},
    {"title": "HR Talent Diagram 10", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent10.jpeg"},
]

def make_content(lesson):
    if lesson["type"] == "image":
        return f'<div style="text-align: center; padding: 20px;"><img src="{lesson["url"]}" alt="{lesson["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
    else:
        return f'<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/{lesson["vimeo"]}?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

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
            "content_type": "text" if lesson["type"] == "image" else "embed",
            "content": make_content(lesson),
            "duration_minutes": 5 if lesson["type"] == "image" else 10,
            "order": 122 + i
        })
        print(f"  [{122+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {122 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
