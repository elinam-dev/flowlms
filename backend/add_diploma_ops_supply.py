#!/usr/bin/env python3
"""
Rename diploma_operations_supply_management images by date order,
create the course in DB, add all lessons and publish.
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
IMG_DIR = ROOT_DIR / "uploads" / "images" / "supply_chain" / "diploma_operations_supply_management"

async def setup():
    # Step 1: Rename images by date order
    files = sorted([f for f in IMG_DIR.iterdir() if f.suffix.lower() in ['.jpeg', '.jpg']], key=lambda f: f.stat().st_mtime)
    print(f"Found {len(files)} images, renaming...")
    renamed = []
    for i, f in enumerate(files, 1):
        new_name = f"diploma_ops_supply_{i:03d}.jpeg"
        new_path = IMG_DIR / new_name
        if f.name != new_name:
            f.rename(new_path)
        renamed.append(new_name)

    print(f"Renamed {len(renamed)} images")

    # Step 2: Create course if it doesn't exist
    existing = await db.courses.find_one({'title': {'$regex': 'diploma in operations and supply', '$options': 'i'}})
    if not existing:
        course_id = str(uuid.uuid4())
        await db.courses.insert_one({
            "id": course_id,
            "title": "Diploma in Operations and Supply Management",
            "description": "Comprehensive training in operations and supply chain management covering procurement, logistics, inventory management, and strategic planning.",
            "category": "Supply Chain",
            "course_type": "optional",
            "duration_hours": 20,
            "is_published": True,
            "enrolled_users": [],
            "created_at": "2024-01-01T00:00:00"
        })
        print(f"Created course")
    else:
        course_id = existing["id"]
        await db.courses.update_one({"id": course_id}, {"$set": {"is_published": True}})
        print(f"Found existing course: {existing['title']}")

    # Step 3: Create module
    module = await db.modules.find_one({"course_id": course_id})
    if not module:
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course_id,
            "title": "Course Content",
            "order": 0
        })
        module = await db.modules.find_one({"id": module_id})
    else:
        await db.lessons.delete_many({"module_id": module["id"]})

    # Step 4: Add lessons
    for i, filename in enumerate(renamed):
        url = f"{BASE_URL}/uploads/images/supply_chain/diploma_operations_supply_management/{filename}"
        content = f'<div style="text-align: center; padding: 20px;"><img src="{url}" alt="Slide {i+1}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": f"Slide {i+1}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 3,
            "order": i
        })

    print(f"Added {len(renamed)} lessons and published the course.")

if __name__ == "__main__":
    asyncio.run(setup())
