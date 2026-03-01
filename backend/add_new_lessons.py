#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

LESSONS = [
    {"title": "Supply Chain Networks - Part 1", "url": "https://player.vimeo.com/video/95264460?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Networks - Part 2", "url": "https://player.vimeo.com/video/95265089?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Networks - Part 3", "url": "https://player.vimeo.com/video/95265721?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Networks - Part 4", "url": "https://player.vimeo.com/video/95266193?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Networks - Part 5", "url": "https://player.vimeo.com/video/95266946?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Networks - Part 6", "url": "https://player.vimeo.com/video/95267682?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Zara - Part 1", "url": "https://player.vimeo.com/video/95268164?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Zara - Part 2", "url": "https://player.vimeo.com/video/95269176?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Zara - Part 3", "url": "https://player.vimeo.com/video/95270183?quality=720p&audiotrack=main&texttrack=en"}
]

async def add_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"], "title": "Course Content"})
    
    for i, lesson_data in enumerate(LESSONS, start=1):
        content = f'<div style="text-align: center;"><iframe src="{lesson_data["url"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson_data["title"],
            "content_type": "embed",
            "content": content,
            "duration_minutes": 10,
            "order": i
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"Added: {lesson_data['title']}")
    
    print(f"\nAdded {len(LESSONS)} lessons")

if __name__ == "__main__":
    asyncio.run(add_lessons())
