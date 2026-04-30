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

async def check():
    course = await db.courses.find_one(
        {'title': {'$regex': 'talent management and workforce', '$options': 'i'}},
        {'_id': 0, 'id': 1, 'title': 1, 'is_published': 1}
    )
    print(f"Title: {course['title']}")
    print(f"Published: {course['is_published']}")

    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_ids = [m['id'] for m in modules]
    lessons = await db.lessons.find({'module_id': {'$in': module_ids}}).sort('order', 1).to_list(None)
    print(f"Total lessons: {len(lessons)}")
    for l in lessons:
        src = ''
        if 'src=' in l['content']:
            start = l['content'].find('src="') + 5
            end = l['content'].find('"', start)
            src = l['content'][start:end][-60:]
        print(f"  order={l['order']} | {l['title']} | {src}")

if __name__ == "__main__":
    asyncio.run(check())
