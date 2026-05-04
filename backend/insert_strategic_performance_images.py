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

async def fix():
    course = await db.courses.find_one(
        {'title': {'$regex': 'diploma in strategic performance', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_ids = [m['id'] for m in modules]
    module_id = modules[0]['id']

    # Shift all lessons with order >= 39 up by 3
    lessons_to_shift = await db.lessons.find(
        {'module_id': {'$in': module_ids}, 'order': {'$gte': 39}}
    ).to_list(None)

    for lesson in lessons_to_shift:
        await db.lessons.update_one(
            {'_id': lesson['_id']},
            {'$set': {'order': lesson['order'] + 3}}
        )
    print(f"Shifted {len(lessons_to_shift)} lessons up by 3")

    # Insert 3 images at positions 39, 40, 41
    images = [
        {"order": 39, "title": "Strategic Performance Diagram 8", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_008.jpeg"},
        {"order": 40, "title": "Strategic Performance Diagram 9", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_009.jpeg"},
        {"order": 41, "title": "Strategic Performance Diagram 10", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_010.jpeg"},
    ]

    for img in images:
        content = f'<div style="text-align: center; padding: 20px;"><img src="{img["url"]}" alt="{img["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": img["title"],
            "content_type": "text",
            "content": content,
            "duration_minutes": 5,
            "order": img["order"]
        })
        print(f"  Inserted [{img['order']}] {img['title']}")

    print("\nDone!")

if __name__ == "__main__":
    asyncio.run(fix())
