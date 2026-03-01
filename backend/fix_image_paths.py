#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def fix_image_paths():
    """Convert absolute Windows paths to relative URLs"""
    
    # Find all lessons with image content
    lessons = await db.lessons.find({
        "$or": [
            {"content_type": "image"},
            {"content": {"$regex": "C:\\\\Users"}}
        ]
    }).to_list(None)
    
    updated = 0
    for lesson in lessons:
        content = lesson.get("content", "")
        
        # Replace absolute paths with relative URLs
        if "C:\\Users\\User\\Desktop\\flowlms\\flowlms\\backend\\uploads" in content:
            # For image type lessons
            if lesson.get("content_type") == "image":
                # Extract filename
                filename = content.split("\\")[-1]
                folder = content.split("\\")[-2]
                new_url = f"/uploads/images/{folder}/{filename}"
                
                await db.lessons.update_one(
                    {"id": lesson["id"]},
                    {"$set": {"content": new_url}}
                )
                print(f"Updated {lesson['title']}: {new_url}")
                updated += 1
            else:
                # For embedded images in HTML content
                new_content = content.replace(
                    'C:\\Users\\User\\Desktop\\flowlms\\flowlms\\backend\\uploads\\images\\diploma in supply chain\\',
                    '/uploads/images/diploma in supply chain/'
                ).replace('\\', '/')
                
                await db.lessons.update_one(
                    {"id": lesson["id"]},
                    {"$set": {"content": new_content}}
                )
                print(f"Updated HTML in {lesson['title']}")
                updated += 1
    
    print(f"\nTotal updated: {updated} lessons")

if __name__ == "__main__":
    asyncio.run(fix_image_paths())
