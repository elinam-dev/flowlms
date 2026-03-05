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

async def check_image_content():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    modules = await db.modules.find({"course_id": course["id"]}).to_list(None)
    
    for module in modules:
        lessons = await db.lessons.find({"module_id": module["id"]}).sort("order", 1).to_list(None)
        
        for i, lesson in enumerate(lessons, 1):
            content = lesson.get("content", "")
            if "supply" in content.lower() or "img" in content.lower():
                print(f"\nPage {i}: {lesson['title']}")
                print(f"Type: {lesson.get('content_type')}")
                print(f"Content: {content[:200]}")

if __name__ == "__main__":
    asyncio.run(check_image_content())
