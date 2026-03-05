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
    {"title": "International Marketing Diagram 2", "type": "image", "content": "/uploads/images/international_marketing__and_supply_chain_management/internationalmarketing2.jpeg"},
    {"title": "International Marketing Diagram 3", "type": "image", "content": "/uploads/images/international_marketing__and_supply_chain_management/internationalmarketing3.jpeg"},
    {"title": "International Marketing Diagram 4", "type": "image", "content": "/uploads/images/international_marketing__and_supply_chain_management/internationalmarketing4.jpeg"},
    {"title": "International Research Survey Methods", "type": "embed", "content": "https://player.vimeo.com/video/911771458?quality=720p&audiotrack=main&texttrack=en"}
]

async def add_final_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "international.*marketing.*supply.*chain", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    start_order = 11
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
    asyncio.run(add_final_lessons())
