#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import re

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def remove_module_numbers():
    """Remove module numbers like 1.1, 2.2, etc. from lesson titles"""
    
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    if not course:
        print("Course not found!")
        return
    
    modules = await db.modules.find({"course_id": course["id"]}).to_list(None)
    
    updated = 0
    for module in modules:
        lessons = await db.lessons.find({"module_id": module["id"]}).to_list(None)
        
        for lesson in lessons:
            title = lesson.get("title", "")
            # Remove patterns like "1.1 ", "2.2 ", "10.1 ", etc.
            new_title = re.sub(r'^\d+\.\d+\s+', '', title)
            
            if new_title != title:
                await db.lessons.update_one(
                    {"id": lesson["id"]},
                    {"$set": {"title": new_title}}
                )
                print(f"Updated: '{title}' -> '{new_title}'")
                updated += 1
    
    print(f"\nTotal updated: {updated} lessons")

if __name__ == "__main__":
    asyncio.run(remove_module_numbers())
