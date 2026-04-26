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
IMG_DIR = ROOT_DIR / "uploads" / "images" / "HR" / "strategic_performance_management"

async def add_lessons():
    files = sorted([f for f in IMG_DIR.iterdir() if f.suffix.lower() in ['.jpeg', '.jpg']])
    renamed = []
    for i, f in enumerate(files, 1):
        new_name = f"strategic_performance_{i:03d}.jpeg"
        new_path = IMG_DIR / new_name
        if f.name != new_name:
            f.rename(new_path)
        renamed.append(new_name)
        print(f"  {f.name} -> {new_name}")

    course = await db.courses.find_one({"title": {"$regex": "diploma in strategic performance", "$options": "i"}}, {"_id": 0})
    if not course:
        print("Course not found!")
        return
    print(f"\nFound: {course['title']}")

    module = await db.modules.find_one({"course_id": course["id"]})
    if not module:
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({"id": module_id, "course_id": course["id"], "title": "Course Content", "order": 0})
        module = await db.modules.find_one({"id": module_id})
    else:
        await db.lessons.delete_many({"module_id": module["id"]})

    for i, filename in enumerate(renamed):
        url = f"{BASE_URL}/uploads/images/HR/strategic_performance_management/{filename}"
        content = f'<div style="text-align: center; padding: 20px;"><img src="{url}" alt="Slide {i+1}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        await db.lessons.insert_one({"id": str(uuid.uuid4()), "module_id": module["id"], "title": f"Slide {i+1}", "content_type": "text", "content": content, "duration_minutes": 3, "order": i})
        print(f"  [{i+1}] {filename}")

    await db.courses.update_one({"id": course["id"]}, {"$set": {"is_published": True}})
    print(f"\nAdded {len(renamed)} lesson(s) and published the course.")

if __name__ == "__main__":
    asyncio.run(add_lessons())
