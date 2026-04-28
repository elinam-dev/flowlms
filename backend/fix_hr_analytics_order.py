#!/usr/bin/env python3
"""
Rename hr_analytics images in correct date order and update lesson content URLs
"""
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
    # Get files sorted by date modified (original order)
    files = sorted(IMG_DIR.iterdir(), key=lambda f: f.stat().st_mtime)
    files = [f for f in files if f.suffix.lower() in ['.jpeg', '.jpg']]
    print(f"Found {len(files)} images in date order")

    # Rename to temp names first to avoid conflicts
    temp_map = {}
    for i, f in enumerate(files):
        temp_name = f"temp_{i:03d}.jpeg"
        temp_path = IMG_DIR / temp_name
        f.rename(temp_path)
        temp_map[temp_name] = i + 1

    # Rename from temp to final names
    final_names = []
    for temp_name, num in temp_map.items():
        temp_path = IMG_DIR / temp_name
        final_name = f"hr_analytics_slide_{num:03d}.jpeg"
        final_path = IMG_DIR / final_name
        temp_path.rename(final_path)
        final_names.append(final_name)
        print(f"  {temp_name} -> {final_name}")

    # Update lessons in DB
    course = await db.courses.find_one(
        {'title': {'$regex': 'hr analytics', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_ids = [m['id'] for m in modules]

    # Delete existing lessons and recreate in correct order
    await db.lessons.delete_many({'module_id': {'$in': module_ids}})

    final_names_sorted = sorted(final_names)
    for i, filename in enumerate(final_names_sorted):
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

    print(f"\nRebuilt {len(final_names_sorted)} lessons in correct order.")

if __name__ == "__main__":
    asyncio.run(fix())
