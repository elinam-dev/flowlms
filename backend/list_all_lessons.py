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

async def list_all_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    modules = await db.modules.find({"course_id": course["id"]}).sort("order", 1).to_list(None)
    
    page_num = 1
    for module in modules:
        print(f"\n=== {module['title']} ===")
        lessons = await db.lessons.find({"module_id": module["id"]}).sort("order", 1).to_list(None)
        
        for lesson in lessons:
            content = lesson.get("content", "")[:150]
            print(f"\nPage {page_num}: {lesson['title']}")
            print(f"  Type: {lesson.get('content_type')}")
            print(f"  Content: {content}...")
            page_num += 1

if __name__ == "__main__":
    asyncio.run(list_all_lessons())
