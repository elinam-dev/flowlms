#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE_URL = "https://flowlms-production.up.railway.app"

LESSONS = [
    {"title": "HR Talent Diagram 3", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent03.jpeg"},
    {"title": "Access the Training Module Manual", "type": "embed", "content": "https://player.vimeo.com/video/880254128?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "An Overview of Recruitment", "type": "embed", "content": "https://player.vimeo.com/video/880254468?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Recruitment", "type": "embed", "content": "https://player.vimeo.com/video/880253605?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Selection Process Optimization", "type": "embed", "content": "https://player.vimeo.com/video/880254737?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Selection Optimization", "type": "embed", "content": "https://player.vimeo.com/video/880254789?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Recruitment Goal Setting", "type": "embed", "content": "https://player.vimeo.com/video/880262506?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Goal Setting", "type": "embed", "content": "https://player.vimeo.com/video/880261255?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "The Interview", "type": "embed", "content": "https://player.vimeo.com/video/880261936?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: The Interview", "type": "embed", "content": "https://player.vimeo.com/video/880262029?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Contract Negotiations", "type": "embed", "content": "https://player.vimeo.com/video/880295943?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Interview Questions", "type": "embed", "content": "https://player.vimeo.com/video/880261747?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "The Selection Process", "type": "embed", "content": "https://player.vimeo.com/video/880267131?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Selection", "type": "embed", "content": "https://player.vimeo.com/video/880266017?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Vital Background Check", "type": "embed", "content": "https://player.vimeo.com/video/880266864?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Background Check", "type": "embed", "content": "https://player.vimeo.com/video/880266349?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Contract Amendments", "type": "embed", "content": "https://player.vimeo.com/video/880298110?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Job Offers", "type": "embed", "content": "https://player.vimeo.com/video/880266015?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Engaging Orientation", "type": "embed", "content": "https://player.vimeo.com/video/880268500?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Orientation", "type": "embed", "content": "https://player.vimeo.com/video/880267679?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Measuring Recruitment Results", "type": "embed", "content": "https://player.vimeo.com/video/880267778?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Measuring Results", "type": "embed", "content": "https://player.vimeo.com/video/880267836?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Module 2 Wrapping Up", "type": "embed", "content": "https://player.vimeo.com/video/880269730?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "HR Talent Diagram 4", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent04.jpeg"},
]

def make_content(lesson):
    if lesson["type"] == "image":
        return f'<div style="text-align: center; padding: 20px;"><img src="{lesson["content"]}" alt="{lesson["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
    else:
        return f'<div style="text-align: center;"><iframe src="{lesson["content"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def add():
    course = await db.courses.find_one(
        {'title': {'$regex': 'talent management and workforce', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_id = modules[0]['id']

    for i, lesson in enumerate(LESSONS):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": lesson["title"],
            "content_type": "text" if lesson["type"] == "image" else "embed",
            "content": make_content(lesson),
            "duration_minutes": 5 if lesson["type"] == "image" else 10,
            "order": 25 + i
        })
        print(f"  [{25+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {25 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
