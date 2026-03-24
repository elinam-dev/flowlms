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
    {"title": "Brief Introduction to Sea Export", "type": "embed", "content": "https://player.vimeo.com/video/855099123?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Overview of Sea Export Forwarding", "type": "embed", "content": "https://player.vimeo.com/video/855099994?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Key Players in Sea Export Forwarding", "type": "embed", "content": "https://player.vimeo.com/video/855101879?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Product Sourcing and Selection", "type": "embed", "content": "https://player.vimeo.com/video/855109114?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Order Management", "type": "embed", "content": "https://player.vimeo.com/video/855108819?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Pre-Shipment Inspection", "type": "embed", "content": "https://player.vimeo.com/video/855117273?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Packaging and Labelling", "type": "embed", "content": "https://player.vimeo.com/video/855117376?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Brief Summary", "type": "embed", "content": "https://player.vimeo.com/video/857048876?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction to Shipping Procedures", "type": "embed", "content": "https://player.vimeo.com/video/855145108?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Booking and Confirmation", "type": "embed", "content": "https://player.vimeo.com/video/855145621?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Bill of Landing (B/L)", "type": "embed", "content": "https://player.vimeo.com/video/855146500?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Export Declaration and Customs Clearance", "type": "embed", "content": "https://player.vimeo.com/video/855147239?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Customs Clearance Procedures", "type": "embed", "content": "https://player.vimeo.com/video/855149648?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Quick Recap", "type": "embed", "content": "https://player.vimeo.com/video/855150233?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Sea Export Diagram 1", "type": "image", "content": "/uploads/images/sea_export/sea_export2.jpeg"},
    {"title": "Sea Export Diagram 2", "type": "image", "content": "/uploads/images/sea_export/sea_export3.jpeg"}
]

async def add_sea_export_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "complete.*guide.*sea.*export.*forwarding", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    # Update first lesson with image
    lesson1 = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Introduction"
    })
    
    if lesson1:
        content = '<div style="text-align: center; padding: 20px;"><img src="/uploads/images/sea_export/sea_export1.jpeg" alt="Introduction" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        await db.lessons.update_one(
            {"id": lesson1["id"]},
            {"$set": {"content": content, "content_type": "text"}}
        )
        print(f"Updated: Introduction with sea_export1.jpeg")
    
    # Add remaining lessons
    for i, lesson_data in enumerate(LESSONS, start=1):
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
            "order": i
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"Added: {lesson_data['title']}")
    
    print(f"\nAdded {len(LESSONS)} lessons")

if __name__ == "__main__":
    asyncio.run(add_sea_export_lessons())
