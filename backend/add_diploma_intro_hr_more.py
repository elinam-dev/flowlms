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
    {"title": "Topic 12", "vimeo": "1094767706"},
    {"title": "Topic 13", "vimeo": "1094767763"},
    {"title": "Topic 14", "vimeo": "1094767889"},
    {"title": "Topic 15", "vimeo": "1094768021"},
    {"title": "Topic 16", "vimeo": "1094768138"},
    {"title": "Topic 17", "vimeo": "1094768233"},
    {"title": "Topic 18", "vimeo": "1094768415"},
    {"title": "Topic 19", "vimeo": "1094768564"},
    {"title": "Topic 20", "vimeo": "1094768688"},
    {"title": "Topic 21", "vimeo": "1094768790"},
    {"title": "Topic 22", "vimeo": "1094768882"},
    {"title": "Topic 23", "vimeo": "1094768999"},
    {"title": "Topic 24", "vimeo": "1094769079"},
    {"title": "Topic 25", "vimeo": "1094769229"},
    {"title": "Topic 26", "vimeo": "1094769343"},
    {"title": "Topic 27", "vimeo": "1094769443"},
    {"title": "Topic 28", "vimeo": "1094769541"},
    {"title": "Topic 29", "vimeo": "1094769630"},
    {"title": "Topic 30", "vimeo": "1094769817"},
    {"title": "Topic 31", "vimeo": "1094769880"},
    {"title": "Topic 32", "vimeo": "1094769921"},
]

def make_content(vimeo_id):
    return f'<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/{vimeo_id}?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def add():
    course = await db.courses.find_one(
        {'title': {'$regex': 'diploma in introduction to human resource', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_id = modules[0]['id']

    # Start from order 11
    for i, lesson in enumerate(LESSONS):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": lesson["title"],
            "content_type": "embed",
            "content": make_content(lesson["vimeo"]),
            "duration_minutes": 10,
            "order": 11 + i
        })
        print(f"  Added {lesson['title']} (order={11+i}) -> Vimeo {lesson['vimeo']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {11 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
