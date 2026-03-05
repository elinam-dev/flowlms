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
    {"title": "Introduction", "url": "https://player.vimeo.com/video/868098140?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "The Freight Brokerage Industry", "url": "https://player.vimeo.com/video/868099472?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Roles and Responsibilities of a Freight Brokerage", "url": "https://player.vimeo.com/video/868099504?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain and Logistics", "url": "https://player.vimeo.com/video/868099736?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "url": "https://player.vimeo.com/video/868098007?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction", "url": "https://player.vimeo.com/video/868103355?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Licensing and Bonding Requirements", "url": "https://player.vimeo.com/video/868104066?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Financial Bonding Requirements", "url": "https://player.vimeo.com/video/868103733?quality=720p&audiotrack=main&texttrack=en"}
]

async def add_freight_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "freight.*broker.*training", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    # Update first lesson with image
    lesson1 = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Introduction"
    })
    
    if lesson1:
        content = '<div style="text-align: center; padding: 20px;"><img src="/uploads/images/freight/freight1.jpeg" alt="Introduction" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        await db.lessons.update_one(
            {"id": lesson1["id"]},
            {"$set": {"content": content, "content_type": "text"}}
        )
        print(f"Updated: Introduction with freight1.jpeg")
    
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
    asyncio.run(add_freight_lessons())
