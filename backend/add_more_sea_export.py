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
    {"title": "Sea Export Diagram 3", "type": "image", "content": "/uploads/images/sea_export/sea_export4.jpeg"},
    {"title": "Brief Preface", "type": "embed", "content": "https://player.vimeo.com/video/855152423?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction to Import Clearance", "type": "embed", "content": "https://player.vimeo.com/video/855155259?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Import Haulage Procedures", "type": "embed", "content": "https://player.vimeo.com/video/855156061?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cargo Tracking", "type": "embed", "content": "https://player.vimeo.com/video/855157428?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Documentation Requirements", "type": "embed", "content": "https://player.vimeo.com/video/855168457?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Dealing with Shipping Delays and Problems", "type": "embed", "content": "https://player.vimeo.com/video/855170341?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Topic Highlights", "type": "embed", "content": "https://player.vimeo.com/video/855170637?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introducing Sea Export Forwarding Regulations", "type": "embed", "content": "https://player.vimeo.com/video/855175325?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Importing and Exporting Country Regulations", "type": "embed", "content": "https://player.vimeo.com/video/855176417?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Environmental and Ethical Standards", "type": "embed", "content": "https://player.vimeo.com/video/855177628?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Risk Management", "type": "embed", "content": "https://player.vimeo.com/video/855177711?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Lesson in a Nutshell", "type": "embed", "content": "https://player.vimeo.com/video/855177856?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introducing Future Trends and Technology", "type": "embed", "content": "https://player.vimeo.com/video/855182143?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Tech and Innovation in Sea Export Forwarding", "type": "embed", "content": "https://player.vimeo.com/video/855183135?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Sustainability in Sea Export Forwarding", "type": "embed", "content": "https://player.vimeo.com/video/855216050?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Career Opportunities and Skill Development", "type": "embed", "content": "https://player.vimeo.com/video/855216130?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Quick Recap", "type": "embed", "content": "https://player.vimeo.com/video/855216677?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Sea Export Diagram 4", "type": "image", "content": "/uploads/images/sea_export/sea_export5.jpeg"},
    {"title": "Sea Export Diagram 5", "type": "image", "content": "/uploads/images/sea_export/sea_export6.jpeg"}
]

async def add_more_sea_export():
    course = await db.courses.find_one({
        "title": {"$regex": "complete.*guide.*sea.*export.*forwarding", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    start_order = 17
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
    asyncio.run(add_more_sea_export())
