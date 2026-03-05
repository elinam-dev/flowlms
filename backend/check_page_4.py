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

async def check_page_4():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    modules = await db.modules.find({"course_id": course["id"]}).sort("order", 1).to_list(None)
    
    page_num = 1
    for module in modules:
        lessons = await db.lessons.find({"module_id": module["id"]}).sort("order", 1).to_list(None)
        
        for lesson in lessons:
            if page_num == 4:
                print(f"Page 4: {lesson['title']}")
                print(f"Type: {lesson.get('content_type')}")
                print(f"\nFull Content:")
                print(lesson.get('content', ''))
                return
            page_num += 1

if __name__ == "__main__":
    asyncio.run(check_page_4())
