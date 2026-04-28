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
IMG_DIR = ROOT_DIR / "uploads" / "images" / "HR" / "hr_analytics"

async def fix():
    # Get files sorted by date modified (the order you added them)
    files = sorted(
        [f for f in IMG_DIR.iterdir() if f.suffix.lower() in ['.jpeg', '.jpg']],
        key=lambda f: f.stat().st_mtime
    )
    print(f"Found {len(files)} images")

    # Rename to final names
    renamed = []
    for i, f in enumerate(files, 1):
        new_name = f"hr_analytics_slide_{i:03d}.jpeg"
        new_path = IMG_DIR / new_name
        f.rename(new_path)
        renamed.append(new_name)
        print(f"  {f.name} -> {new_name}")

    # Rebuild lessons
    course = await db.courses.find_one(
        {'title': {'$regex': 'hr analytics', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_ids = [m['id'] for m in modules]
    await db.lessons.delete_many({'module_id': {'$in': module_ids}})

    for i, filename in enumerate(renamed):
        url = f"{BASE_URL}/uploads/images/HR/hr_analytics/{filename}"
        content = f'<div style="text-align: center; padding: 20px;"><img src="{url}" alt="Slide {i+1}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": modules[0]["id"],
            "title": f"Slide {i+1}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 3,
            "order": i
        })

    print(f"\nRenamed {len(renamed)} images and rebuilt {len(renamed)} lessons.")

if __name__ == "__main__":
    asyncio.run(fix())
