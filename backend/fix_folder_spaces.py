#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import shutil

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def fix_folder_and_urls():
    """Rename folder to remove spaces and update database"""
    
    old_folder = ROOT_DIR / "uploads" / "images" / "diploma in supply chain"
    new_folder = ROOT_DIR / "uploads" / "images" / "diploma-supply-chain"
    
    # Rename folder
    if old_folder.exists() and not new_folder.exists():
        shutil.move(str(old_folder), str(new_folder))
        print(f"Renamed folder: {new_folder.name}")
    
    # Update database
    lessons = await db.lessons.find({
        "content": {"$regex": "diploma in supply chain"}
    }).to_list(None)
    
    updated = 0
    for lesson in lessons:
        content = lesson.get("content", "")
        new_content = content.replace(
            "/uploads/images/diploma in supply chain/",
            "/uploads/images/diploma-supply-chain/"
        )
        
        if new_content != content:
            await db.lessons.update_one(
                {"id": lesson["id"]},
                {"$set": {"content": new_content}}
            )
            print(f"Updated: {lesson['title']}")
            updated += 1
    
    print(f"\nTotal updated: {updated} lessons")

if __name__ == "__main__":
    asyncio.run(fix_folder_and_urls())
