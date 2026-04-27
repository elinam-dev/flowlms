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
        {'title': {'$regex': 'introduction to modern human', '$options': 'i'}},
        {'_id': 0, 'id': 1, 'title': 1}
    )
    print(f"Course: {course['title']}")
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_ids = [m['id'] for m in modules]
    lessons = await db.lessons.find({'module_id': {'$in': module_ids}}).sort('order', 1).limit(3).to_list(3)
    for l in lessons:
        print(f"\nLesson: {l['title']}")
        print(f"Content snippet: {l['content'][:200]}")

if __name__ == "__main__":
    asyncio.run(check())
