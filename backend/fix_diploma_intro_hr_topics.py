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

UPDATES = [
    {"order": 7, "title": "Topic 8",  "vimeo": "1094767362"},
    {"order": 8, "title": "Topic 9",  "vimeo": "1094767478"},
    {"order": 9, "title": "Topic 10", "vimeo": "1094767524"},
]
NEW_LESSON = {"order": 10, "title": "Topic 11", "vimeo": "1094767628"}

def make_content(vimeo_id):
    return f'<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/{vimeo_id}?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def fix():
    course = await db.courses.find_one(
        {'title': {'$regex': 'diploma in introduction to human resource', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_ids = [m['id'] for m in modules]

    # Update existing lessons
    for u in UPDATES:
        lesson = await db.lessons.find_one({'module_id': {'$in': module_ids}, 'order': u['order']})
        await db.lessons.update_one(
            {"_id": lesson["_id"]},
            {"$set": {"title": u['title'], "content": make_content(u['vimeo'])}}
        )
        print(f"Updated {u['title']} (order={u['order']}) -> Vimeo {u['vimeo']}")

    # Add Topic 11 as new lesson
    await db.lessons.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": modules[0]["id"],
        "title": NEW_LESSON["title"],
        "content_type": "embed",
        "content": make_content(NEW_LESSON["vimeo"]),
        "duration_minutes": 10,
        "order": NEW_LESSON["order"]
    })
    print(f"Added {NEW_LESSON['title']} (order={NEW_LESSON['order']}) -> Vimeo {NEW_LESSON['vimeo']}")

if __name__ == "__main__":
    asyncio.run(fix())
