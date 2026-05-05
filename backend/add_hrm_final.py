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

async def add():
    course = await db.courses.find_one(
        {'title': {'$regex': 'ultimate employee onboarding', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_id = modules[0]['id']

    for i, num in enumerate([36, 37]):
        url = f"{BASE_URL}/uploads/images/HR/HRM/hrm_{num:03d}.jpeg"
        content = f'<div style="text-align: center; padding: 20px;"><img src="{url}" alt="Slide {40+i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": f"Slide {40+i}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 5,
            "order": 41 + i
        })
        print(f"  [{41+i}] Slide {40+i} -> hrm_{num:03d}.jpeg")

    print("\nDone! Course now has 43 total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
