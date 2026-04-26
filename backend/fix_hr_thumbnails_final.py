#!/usr/bin/env python3
"""
1. Assign 18 cover images to exactly the 18 hr category courses
2. Update lesson image URLs for the 2 moved folders
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

async def fix():
    # Get images from HR root only
    images = sorted([f.name for f in HR_IMG_DIR.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
    print(f"Found {len(images)} cover images")

    # Get exactly the 18 hr category courses
    courses = await db.courses.find(
        {'category': 'hr'},
        {'_id': 0, 'id': 1, 'title': 1}
    ).sort('title', 1).to_list(None)
    print(f"Found {len(courses)} hr courses")

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

    # Update lesson URLs for moved folders
    old_perf = "/uploads/images/HR/performance_management_system/"
    new_perf = "/uploads/images/performance_management_system/"
    old_beh = "/uploads/images/HR/behavioral_interviewing/"
    new_beh = "/uploads/images/behavioral_interviewing/"

    lessons = await db.lessons.find({"content": {"$regex": "HR/performance_management_system|HR/behavioral_interviewing"}}).to_list(None)
    for lesson in lessons:
        new_content = lesson["content"].replace(old_perf, new_perf).replace(old_beh, new_beh)
        await db.lessons.update_one({"_id": lesson["_id"]}, {"$set": {"content": new_content}})
    print(f"\nUpdated {len(lessons)} lesson URLs for moved folders")
    print("\nDone!")

if __name__ == "__main__":
    asyncio.run(fix())
