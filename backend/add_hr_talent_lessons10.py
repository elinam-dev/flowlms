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
    {"title": "HR Talent Diagram 14", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent14.jpeg"},
    {"title": "Module 8 - Getting Started", "type": "embed", "vimeo": "880618885"},
    {"title": "Kolb's Learning Styles", "type": "embed", "vimeo": "880621449"},
    {"title": "Case Study: Learning Variation", "type": "embed", "vimeo": "880619425"},
    {"title": "Kirkpatrick's Evaluation Levels", "type": "embed", "vimeo": "880622415"},
    {"title": "Case Study: Evaluation Levels", "type": "embed", "vimeo": "880619738"},
    {"title": "Managing Performance", "type": "embed", "vimeo": "880331902"},
    {"title": "Case Study: Measurement Tools", "type": "embed", "vimeo": "880620032"},
    {"title": "Targeted Training", "type": "embed", "vimeo": "880620023"},
    {"title": "Case Study: Targeted Training", "type": "embed", "vimeo": "880620108"},
    {"title": "Creating an Evaluation Plan", "type": "embed", "vimeo": "919772047"},
    {"title": "Case Study: Evaluation Plan", "type": "embed", "vimeo": "880620098"},
    {"title": "Pre-Training Evaluation", "type": "embed", "vimeo": "880624469"},
    {"title": "Case Study: Pre-Training Evaluation", "type": "embed", "vimeo": "880625355"},
    {"title": "Learning Progress Checks", "type": "embed", "vimeo": "880625439"},
    {"title": "Case Study: Progress Checks", "type": "embed", "vimeo": "880625480"},
    {"title": "Post-Training Evaluation", "type": "embed", "vimeo": "880625531"},
    {"title": "Case Study: Post-Training Evaluation", "type": "embed", "vimeo": "880625666"},
    {"title": "Enduring Impact Vision", "type": "embed", "vimeo": "880625724"},
    {"title": "Case Study: Impact Vision", "type": "embed", "vimeo": "880625761"},
    {"title": "Calculating Return on Investment (ROI)", "type": "embed", "vimeo": "880626231"},
    {"title": "Case Study: Calculating ROI", "type": "embed", "vimeo": "880626037"},
    {"title": "Module 8 Wrapping Up", "type": "embed", "vimeo": "880626022"},
    {"title": "HR Talent Diagram 15", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent15.jpeg"},
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
            "order": 176 + i
        })
        print(f"  [{176+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {176 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
