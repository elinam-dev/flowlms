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

VIDEOS = [
    {"title": "Supply Chain Ecosystem - Part 1", "url": "https://player.vimeo.com/video/96488304?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Ecosystem - Part 2", "url": "https://player.vimeo.com/video/96488828?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Ecosystem - Part 3", "url": "https://player.vimeo.com/video/96492369?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Ecosystem - Part 4", "url": "https://player.vimeo.com/video/96493030?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Ecosystem - Part 5", "url": "https://player.vimeo.com/video/96493480?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Ecosystem - Part 6", "url": "https://player.vimeo.com/video/96493480?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Ecosystem - Part 7", "url": "https://player.vimeo.com/video/96495001?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Ecosystem - Part 8", "url": "https://player.vimeo.com/video/96495877?quality=720p&audiotrack=main&texttrack=en"}
]

async def add_ecosystem_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "understanding.*supply.*chain.*ecosystem", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    # Update first lesson with image
    lesson1 = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Introduction"
    })
    
    if lesson1:
        content = '<div style="text-align: center; padding: 20px;"><img src="/uploads/images/understanding_supply_chain_ecosystem_fundamentals_of_using_six_sigma_in_supply_chain/ecosystem1.jpeg" alt="Introduction" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        await db.lessons.update_one(
            {"id": lesson1["id"]},
            {"$set": {"content": content, "content_type": "text"}}
        )
        print(f"Updated: Introduction with ecosystem1.jpeg")
    
    # Add video lessons
    for i, video in enumerate(VIDEOS, start=1):
        content = f'<div style="text-align: center;"><iframe src="{video["url"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": video["title"],
            "content_type": "embed",
            "content": content,
            "duration_minutes": 10,
            "order": i
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"Added: {video['title']}")
    
    print(f"\nDone! Added 8 video lessons")

if __name__ == "__main__":
    asyncio.run(add_ecosystem_lessons())
