#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE_URL = "https://flowlms-production.up.railway.app"

async def fix():
    course = await db.courses.find_one(
        {'title': {'$regex': 'french', '$options': 'i'}},
        {'_id': 0, 'id': 1, 'title': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_ids = [m['id'] for m in modules]
    lessons = await db.lessons.find({'module_id': {'$in': module_ids}}).to_list(None)

    updated = 0
    for lesson in lessons:
        new_content = lesson['content'].replace(
            'http://127.0.0.1:8000/api/uploads/images/french/',
            f'{BASE_URL}/uploads/images/french/'
        ).replace(
            'http://localhost:8000/api/uploads/images/french/',
            f'{BASE_URL}/uploads/images/french/'
        )
        if new_content != lesson['content']:
            await db.lessons.update_one({"_id": lesson["_id"]}, {"$set": {"content": new_content}})
            updated += 1

    print(f"Updated {updated} of {len(lessons)} French lessons")

if __name__ == "__main__":
    asyncio.run(fix())
