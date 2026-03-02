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
    {"title": "Supply Chain Risk - Part 4", "type": "embed", "content": "https://player.vimeo.com/video/104930808?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Risk - Part 5", "type": "embed", "content": "https://player.vimeo.com/video/104931870?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Risk - Part 6", "type": "embed", "content": "https://player.vimeo.com/video/104932733?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Risk - Part 7", "type": "embed", "content": "https://player.vimeo.com/video/104934297?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Risk - Part 8", "type": "embed", "content": "https://player.vimeo.com/video/104935247?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Supply Chain Risk - Part 9", "type": "embed", "content": "https://player.vimeo.com/video/104936154?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Risk Management Diagram 1", "type": "image", "content": "/uploads/images/understanding-supply-risk-management/supplyrisk2.jpeg"},
    {"title": "Risk Management Diagram 2", "type": "image", "content": "/uploads/images/understanding-supply-risk-management/supplyrisk3.jpeg"},
    {"title": "Risk Management Diagram 3", "type": "image", "content": "/uploads/images/understanding-supply-risk-management/supplyrisk4.jpeg"},
    {"title": "Risk Management Diagram 4", "type": "image", "content": "/uploads/images/understanding-supply-risk-management/supplyrisk5.jpeg"},
    {"title": "Risk Management Diagram 5", "type": "image", "content": "/uploads/images/understanding-supply-risk-management/supplyrisk6.jpeg"},
    {"title": "Risk Management Diagram 6", "type": "image", "content": "/uploads/images/understanding-supply-risk-management/supplyrisk7.jpeg"},
    {"title": "Risk Management Diagram 7", "type": "image", "content": "/uploads/images/understanding-supply-risk-management/supplyrisk8.jpeg"}
]

async def add_remaining_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "understanding.*supply.*chain.*risk", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    start_order = 3
    for i, lesson_data in enumerate(LESSONS):
        if lesson_data["type"] == "embed":
            content = f'<div style="text-align: center;"><iframe src="{lesson_data["content"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
        else:
            content = lesson_data["content"]
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson_data["title"],
            "content_type": lesson_data["type"],
            "content": content,
            "duration_minutes": 10 if lesson_data["type"] == "embed" else 5,
            "order": start_order + i
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"Added: {lesson_data['title']}")
    
    print(f"\nAdded {len(LESSONS)} lessons")

if __name__ == "__main__":
    asyncio.run(add_remaining_lessons())
