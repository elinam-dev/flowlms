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
    {"title": "HR Talent Diagram 11", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent11.jpeg"},
    {"title": "Module 6 - Getting Started", "type": "embed", "vimeo": "880330894"},
    {"title": "Defining Talent", "type": "embed", "vimeo": "880329835"},
    {"title": "Case Study: Defining Talent", "type": "embed", "vimeo": "918090471"},
    {"title": "Overview of Talent", "type": "embed", "vimeo": "880329920"},
    {"title": "Case Study: Overview of Talent", "type": "embed", "vimeo": "880329975"},
    {"title": "Managing Performance", "type": "embed", "vimeo": "880331902"},
    {"title": "Case Study: Managing Performance", "type": "embed", "vimeo": "880331939"},
    {"title": "Talent Reviews", "type": "embed", "vimeo": "880331976"},
    {"title": "Case Study: Talent Reviews", "type": "embed", "vimeo": "880331996"},
    {"title": "Succession and Planning", "type": "embed", "vimeo": "880341536"},
    {"title": "Case Study: Succession", "type": "embed", "vimeo": "880340250"},
    {"title": "Enhancing Engagement", "type": "embed", "vimeo": "880333009"},
    {"title": "Case Study: Enhancing Engagement", "type": "embed", "vimeo": "880333125"},
    {"title": "Competency Assessment", "type": "embed", "vimeo": "880333146"},
    {"title": "Case Study: Competency Assessment", "type": "embed", "vimeo": "880333204"},
    {"title": "Guiding Growth", "type": "embed", "vimeo": "880342434"},
    {"title": "Case Study: Growth", "type": "embed", "vimeo": "880333263"},
    {"title": "Talent Management Best Practices", "type": "embed", "vimeo": "880334006"},
    {"title": "Case Study: Best Practices", "type": "embed", "vimeo": "880334312"},
    {"title": "Employee Retention", "type": "embed", "vimeo": "880334111"},
    {"title": "Case Study: Retention", "type": "embed", "vimeo": "880334172"},
    {"title": "Module 6 - Wrapping Up", "type": "embed", "vimeo": "880299529"},
]

def make_content(lesson):
    if lesson["type"] == "image":
        return f'<div style="text-align: center; padding: 20px;"><img src="{lesson["url"]}" alt="{lesson["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
    else:
        return f'<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/{lesson["vimeo"]}?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

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
            "order": 129 + i
        })
        print(f"  [{129+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {129 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
