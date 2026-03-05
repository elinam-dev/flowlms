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
    {"title": "Federal Motor Carrier Safety Administration", "type": "embed", "content": "https://player.vimeo.com/video/868104673?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "The Unified Carrier Registration (UCR) Programme", "type": "embed", "content": "https://player.vimeo.com/video/868104448?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "type": "embed", "content": "https://player.vimeo.com/video/868103550?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction", "type": "embed", "content": "https://player.vimeo.com/video/868107957?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Prospecting and Acquiring Customers", "type": "embed", "content": "https://player.vimeo.com/video/868116309?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Customer Acquisition Strategies", "type": "embed", "content": "https://player.vimeo.com/video/868116365?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Negotiating Rates and Contracts", "type": "embed", "content": "https://player.vimeo.com/video/868115471?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Freight Pricing Strategies", "type": "embed", "content": "https://player.vimeo.com/video/868115136?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Load Planning and Routing", "type": "embed", "content": "https://player.vimeo.com/video/868112482?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "type": "embed", "content": "https://player.vimeo.com/video/868111401?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "type": "embed", "content": "https://player.vimeo.com/video/868111401?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction", "type": "embed", "content": "https://player.vimeo.com/video/868117325?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Bill of Landing (BOL)", "type": "embed", "content": "https://player.vimeo.com/video/868119751?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Proper Record Keeping and Documentation", "type": "embed", "content": "https://player.vimeo.com/video/868119095?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Compliance with Financial and Accounting Laws", "type": "embed", "content": "https://player.vimeo.com/video/868119810?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Use of Technology and Software", "type": "embed", "content": "https://player.vimeo.com/video/868120484?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "type": "embed", "content": "https://player.vimeo.com/video/868117367?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Freight Broker Diagram 1", "type": "image", "content": "/uploads/images/freight/freight2.jpeg"},
    {"title": "Freight Broker Diagram 2", "type": "image", "content": "/uploads/images/freight/freight3.jpeg"}
]

async def add_all_freight_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "freight.*broker.*training", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    start_order = 9
    for i, lesson_data in enumerate(LESSONS):
        if lesson_data["type"] == "embed":
            content = f'<div style="text-align: center;"><iframe src="{lesson_data["content"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
        else:
            content = f'<div style="text-align: center; padding: 20px;"><img src="{lesson_data["content"]}" alt="{lesson_data["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson_data["title"],
            "content_type": "text" if lesson_data["type"] == "image" else "embed",
            "content": content,
            "duration_minutes": 10 if lesson_data["type"] == "embed" else 5,
            "order": start_order + i
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"Added: {lesson_data['title']}")
    
    print(f"\nAdded {len(LESSONS)} lessons")

if __name__ == "__main__":
    asyncio.run(add_all_freight_lessons())
