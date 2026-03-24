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
    {"title": "Preparing Basic Financial Statements in the Form of Profit and Loss", "url": "https://player.vimeo.com/video/908007059?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Preparing a Trial Balance, P and L Account and a Balance Sheet", "url": "https://player.vimeo.com/video/908007096?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Income and Expenses", "url": "https://player.vimeo.com/video/908007128?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Matching Concepts", "url": "https://player.vimeo.com/video/908007149?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Concept of Conservatism", "url": "https://player.vimeo.com/video/908007188?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction to Depreciation", "url": "https://player.vimeo.com/video/908007225?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Causes and Methods of Providing Depreciation", "url": "https://player.vimeo.com/video/908007275?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Extract from Tata Motors Annual Report", "url": "https://player.vimeo.com/video/908007350?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction to Inventory Valuation", "url": "https://player.vimeo.com/video/908007443?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Techniques of Inventory Valuation", "url": "https://player.vimeo.com/video/908007492?quality=720p&audiotrack=main&texttrack=en"}
]

async def add_more_videos():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*financial.*accounting", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    start_order = 28
    for i, video in enumerate(VIDEOS):
        content = f'<div style="text-align: center;"><iframe src="{video["url"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": video["title"],
            "content_type": "embed",
            "content": content,
            "duration_minutes": 10,
            "order": start_order + i
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"Added: {video['title']}")
    
    print(f"\nAdded {len(VIDEOS)} video lessons")

if __name__ == "__main__":
    asyncio.run(add_more_videos())
