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
    {"title": "Recommendations for Documentation", "type": "embed", "vimeo": "416827100"},
    {"title": "Characteristics of an Effective Coach & Example", "type": "embed", "vimeo": "416828441"},
    {"title": "Coaching Skills", "type": "embed", "vimeo": "416830843"},
    {"title": "Coaching Evaluation", "type": "embed", "vimeo": "416829982"},
    {"title": "Strategic Performance Diagram 13", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_013.jpeg"},
    {"title": "Strategic Performance Diagram 14", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_014.jpeg"},
    {"title": "Strategic Performance Diagram 15", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_015.jpeg"},
    {"title": "Performance Review", "type": "embed", "vimeo": "416833532"},
    {"title": "Performance Review (Why, Importance & Problems)", "type": "embed", "vimeo": "416832114"},
    {"title": "Why Performance Review", "type": "embed", "vimeo": "416838010"},
    {"title": "Conducting the Appraisal Session", "type": "embed", "vimeo": "416835607"},
    {"title": "Performance Review Discussion (Why)", "type": "embed", "vimeo": "416841106"},
    {"title": "Performance Review Discussion (Process)", "type": "embed", "vimeo": "416839539"},
]

def make_content(lesson):
    if lesson["type"] == "image":
        return f'<div style="text-align: center; padding: 20px;"><img src="{lesson["url"]}" alt="{lesson["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
    else:
        return f'<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/{lesson["vimeo"]}?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def add():
    course = await db.courses.find_one(
        {'title': {'$regex': 'diploma in strategic performance', '$options': 'i'}},
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
            "order": 65 + i
        })
        print(f"  [{65+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {65 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
