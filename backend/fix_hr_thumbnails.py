#!/usr/bin/env python3
"""
Fix HR thumbnails:
- Only assign cover images to 'hr' category courses (not management/HR Policy)
- Restore Disciplinary Code original thumbnail
- Clear wrongly assigned thumbnails from management courses
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

async def fix_thumbnails():
    # Get images from HR root only
    images = sorted([f.name for f in HR_IMG_DIR.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
    print(f"Found {len(images)} cover images")

    # Only get 'hr' category courses sorted by title
    courses = await db.courses.find(
        {'category': 'hr'},
        {'_id': 0, 'id': 1, 'title': 1}
    ).sort('title', 1).to_list(None)
    print(f"Found {len(courses)} hr category courses")

    # Assign one image per hr course
    for i, course in enumerate(courses):
        if i >= len(images):
            print(f"  No image for: {course['title']}")
            break
        img = images[i]
        thumbnail = f"{BASE_URL}/uploads/images/HR/{img}"
        await db.courses.update_one(
            {"id": course["id"]},
            {"$set": {"thumbnail": thumbnail}}
        )
        print(f"  [{i+1}] {course['title'][:55]} -> {img}")

    # Restore Disciplinary Code original thumbnail
    await db.courses.update_one(
        {"title": {"$regex": "disciplinary code", "$options": "i"}},
        {"$set": {"thumbnail": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400&h=225&fit=crop"}}
    )
    print("\nRestored Disciplinary Code thumbnail")

    # Clear thumbnails from management courses that were wrongly assigned
    await db.courses.update_many(
        {"category": "management"},
        {"$set": {"thumbnail": ""}}
    )
    print("Cleared management course thumbnails")

    print("\nDone!")

if __name__ == "__main__":
    asyncio.run(fix_thumbnails())
