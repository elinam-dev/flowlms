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
    {"title": "HR Talent Diagram 12", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent12.jpeg"},
    {"title": "HR Talent Diagram 13", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent13.jpeg"},
    {"title": "Module 7 Getting Started", "type": "embed", "vimeo": "880555553"},
    {"title": "Defining the Position", "type": "embed", "vimeo": "880556257"},
    {"title": "Case Study: Position Defining", "type": "embed", "vimeo": "880556343"},
    {"title": "Hiring Tactics", "type": "embed", "vimeo": "880556493"},
    {"title": "Case Study: Hiring Tactics", "type": "embed", "vimeo": "880556595"},
    {"title": "Attract Top Talent", "type": "embed", "vimeo": "880557878"},
    {"title": "Case Study: Attract Talent", "type": "embed", "vimeo": "880557928"},
    {"title": "Screening for Interviews", "type": "embed", "vimeo": "880558026"},
    {"title": "Screening for Interviews", "type": "embed", "vimeo": "880558080"},
    {"title": "The Interview Stage (I)", "type": "embed", "vimeo": "880559560"},
    {"title": "Case Study: The Interview (I)", "type": "embed", "vimeo": "880559682"},
    {"title": "The Interview Stage (II)", "type": "embed", "vimeo": "880559752"},
    {"title": "Case Study: The Interview (II)", "type": "embed", "vimeo": "880559810"},
    {"title": "The Selection Stage (I)", "type": "embed", "vimeo": "880563705"},
    {"title": "Case Study: The Selection (I)", "type": "embed", "vimeo": "880563285"},
    {"title": "The Selection Stage (II)", "type": "embed", "vimeo": "880563531"},
    {"title": "Case Study: The Selection (II)", "type": "embed", "vimeo": "880563536"},
    {"title": "Crafting the Offer", "type": "embed", "vimeo": "880564142"},
    {"title": "Case Study: Crafting the Offer", "type": "embed", "vimeo": "880563764"},
    {"title": "The Onboarding Stage", "type": "embed", "vimeo": "880563888"},
    {"title": "Case Study: Onboarding", "type": "embed", "vimeo": "880564377"},
    {"title": "Module 7 - Wrapping Up", "type": "embed", "vimeo": "880564220"},
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
            "order": 152 + i
        })
        print(f"  [{152+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {152 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
