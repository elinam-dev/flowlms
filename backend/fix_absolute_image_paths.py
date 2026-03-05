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

async def fix_absolute_paths():
    """Fix absolute Windows paths in lesson content"""
    
    lessons = await db.lessons.find({
        "content": {"$regex": "C:\\\\Users"}
    }).to_list(None)
    
    updated = 0
    for lesson in lessons:
        content = lesson.get("content", "")
        
        # Replace absolute path with relative URL
        new_content = content.replace(
            'C:\\Users\\User\\Desktop\\flowlms\\flowlms\\backend\\uploads\\images\\diploma-supply-chain\\',
            '/uploads/images/diploma-supply-chain/'
        ).replace('\\', '/')
        
        if new_content != content:
            await db.lessons.update_one(
                {"id": lesson["id"]},
                {"$set": {"content": new_content}}
            )
            print(f"Fixed: {lesson['title']}")
            updated += 1
    
    print(f"\nTotal fixed: {updated} lessons")

if __name__ == "__main__":
    asyncio.run(fix_absolute_paths())
