#!/usr/bin/env python3
"""
Assign HR root images as thumbnails to HR and management courses
"""
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
HR_IMG_DIR = ROOT_DIR / "uploads" / "images" / "HR"

async def assign_thumbnails():
    # Get all image files in HR root (not subdirectories)
    images = sorted([f.name for f in HR_IMG_DIR.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
    print(f"Found {len(images)} cover images")

    # Get all HR and management courses sorted by title
    courses = await db.courses.find(
        {'category': {'$in': ['hr', 'HR Policy', 'management']}},
        {'_id': 0, 'id': 1, 'title': 1}
    ).sort('title', 1).to_list(None)
    print(f"Found {len(courses)} HR/management courses")

    for i, course in enumerate(courses):
        if i >= len(images):
            print(f"  No more images for: {course['title']}")
            break
        img = images[i]
        thumbnail = f"{BASE_URL}/uploads/images/HR/{img}"
        await db.courses.update_one(
            {"id": course["id"]},
            {"$set": {"thumbnail": thumbnail}}
        )
        print(f"  [{i+1}] {course['title'][:50]} -> {img}")

    print("\nDone!")

if __name__ == "__main__":
    asyncio.run(assign_thumbnails())
