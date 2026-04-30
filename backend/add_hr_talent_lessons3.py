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
    {"title": "HR Talent Diagram 5", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent05.jpeg"},
    {"title": "Module 3 - Getting Started", "type": "embed", "content": "https://player.vimeo.com/video/880292494?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Access the Module Manual", "type": "embed", "content": "https://player.vimeo.com/video/899884153?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "What Is Contract Management?", "type": "embed", "content": "https://player.vimeo.com/video/880293504?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Understanding Contract Management", "type": "embed", "content": "https://player.vimeo.com/video/880293538?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Legal and Ethical Considerations", "type": "embed", "content": "https://player.vimeo.com/video/880294237?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Legal Considerations", "type": "embed", "content": "https://player.vimeo.com/video/880293670?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Contract Creation", "type": "embed", "content": "https://player.vimeo.com/video/919584441?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Contract Creation", "type": "embed", "content": "https://player.vimeo.com/video/919584767?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Types of Interview Questions", "type": "embed", "content": "https://player.vimeo.com/video/919585264?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Contract Negotiations", "type": "embed", "content": "https://player.vimeo.com/video/919585643?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Assessing Performance", "type": "embed", "content": "https://player.vimeo.com/video/919586895?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Assessing Performance", "type": "embed", "content": "https://player.vimeo.com/video/919587128?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Renewing Contracts", "type": "embed", "content": "https://player.vimeo.com/video/919587681?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Module 3 - Wrapping Up", "type": "embed", "content": "https://player.vimeo.com/video/919776929?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "HR Talent Diagram 6", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent06.jpeg"},
    {"title": "HR Talent Diagram 7", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent07.jpeg"},
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
            "order": 49 + i
        })
        print(f"  [{49+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {49 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
