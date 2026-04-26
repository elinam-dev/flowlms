#!/usr/bin/env python3
"""Publish all hr category courses that have at least 1 lesson"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def publish_all():
    courses = await db.courses.find({'category': 'hr'}, {'_id': 0, 'id': 1, 'title': 1, 'is_published': 1}).to_list(None)
    published = 0
    skipped = 0
    for c in courses:
        # Check if has lessons
        modules = await db.modules.find({'course_id': c['id']}).to_list(None)
        module_ids = [m['id'] for m in modules]
        lesson_count = await db.lessons.count_documents({'module_id': {'$in': module_ids}}) if module_ids else 0
        if lesson_count > 0:
            await db.courses.update_one({'id': c['id']}, {'$set': {'is_published': True}})
            print(f"  [PUB] {c['title']} ({lesson_count} lessons)")
            published += 1
        else:
            print(f"  [---] {c['title']} (no lessons)")
            skipped += 1
    print(f"\nPublished: {published}, Skipped (no lessons): {skipped}")

if __name__ == "__main__":
    asyncio.run(publish_all())
