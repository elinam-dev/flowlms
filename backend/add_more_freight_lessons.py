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
    {"title": "Federal Motor Carrier Safety Administration", "url": "https://player.vimeo.com/video/868104673?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "The Unified Carrier Registration (UCR) Programme", "url": "https://player.vimeo.com/video/868104448?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "url": "https://player.vimeo.com/video/868103550?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction", "url": "https://player.vimeo.com/video/868107957?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Prospecting and Acquiring Customers", "url": "https://player.vimeo.com/video/868116309?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Customer Acquisition Strategies", "url": "https://player.vimeo.com/video/868116365?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Negotiating Rates and Contracts", "url": "https://player.vimeo.com/video/868115471?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Freight Pricing Strategies", "url": "https://player.vimeo.com/video/868115136?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Load Planning and Routing", "url": "https://player.vimeo.com/video/868112482?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "url": "https://player.vimeo.com/video/868111401?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "url": "https://player.vimeo.com/video/868111401?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction", "url": "https://player.vimeo.com/video/868117325?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Bill of Landing (BOL)", "url": "https://player.vimeo.com/video/868119751?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Proper Record Keeping and Documentation", "url": "https://player.vimeo.com/video/868119095?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Compliance with Financial and Accounting Laws", "url": "https://player.vimeo.com/video/868119810?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Use of Technology and Software", "url": "https://player.vimeo.com/video/868120484?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "url": "https://player.vimeo.com/video/868117367?quality=720p&audiotrack=main&texttrack=en"}
]

async def add_more_freight_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "freight.*broker.*training", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    start_order = 9
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
    asyncio.run(add_more_freight_lessons())
