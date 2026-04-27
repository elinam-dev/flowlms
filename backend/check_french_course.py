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
        {'title': {'$regex': 'french', '$options': 'i'}},
        {'_id': 0, 'id': 1, 'title': 1, 'is_published': 1}
    )
    print(f"Course: {course['title']} | Published: {course['is_published']}")

    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    print(f"Modules: {len(modules)}")

    for m in modules:
        lessons = await db.lessons.find({'module_id': m['id']}).sort('order', 1).to_list(None)
        print(f"  Module: {m['title']} - {len(lessons)} lessons")
        for l in lessons[:3]:
            print(f"    [{l.get('content_type')}] {l['title']}")
            print(f"    Content: {l['content'][:150]}")

if __name__ == "__main__":
    asyncio.run(check())
