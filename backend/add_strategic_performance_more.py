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
    {"title": "Understanding Performance Management", "type": "embed", "vimeo": "416536954"},
    {"title": "Defining Performance Management", "type": "embed", "vimeo": "416536436"},
    {"title": "The Performance Management Contribution", "type": "embed", "vimeo": "416538048"},
    {"title": "HR and Purpose of Performance Management", "type": "embed", "vimeo": "416537564"},
    {"title": "Characteristics of an Effective PM System (Part 1)", "type": "embed", "vimeo": "416538777"},
    {"title": "Characteristics of an Effective PM System (Part 2)", "type": "embed", "vimeo": "416539523"},
    {"title": "Performance Management Process & Examples (Part 1)", "type": "embed", "vimeo": "416540011"},
    {"title": "Performance Management Process & Examples (Part 2)", "type": "embed", "vimeo": "416540665"},
    {"title": "Employee Development Plan, Objectives & Examples", "type": "embed", "vimeo": "416541092"},
    {"title": "Identifying Key Performance Areas", "type": "embed", "vimeo": "416541702"},
    {"title": "Strategic Performance Diagram 2", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_002.jpeg"},
    {"title": "Strategic Performance Diagram 3", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_003.jpeg"},
    {"title": "Strategic Performance Diagram 4", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_004.jpeg"},
    {"title": "Understanding Performance Planning", "type": "embed", "vimeo": "416654407"},
    {"title": "The Role of a Performance Plan & Benefits", "type": "embed", "vimeo": "416542161"},
    {"title": "Purpose of Strategic Planning", "type": "embed", "vimeo": "416544369"},
    {"title": "An Overview of Strategic Planning", "type": "embed", "vimeo": "416543141"},
    {"title": "External and Internal Environment & Gap Analysis", "type": "embed", "vimeo": "416543505"},
    {"title": "Mission Statement", "type": "embed", "vimeo": "416544836"},
    {"title": "Vision Statement", "type": "embed", "vimeo": "416545368"},
    {"title": "Goals & Issues in Goal Setting", "type": "embed", "vimeo": "416545953"},
    {"title": "Strategies, Types of Strategies & Examples", "type": "embed", "vimeo": "416546497"},
    {"title": "Strategy and Performance Alignment (Part 1)", "type": "embed", "vimeo": "416547256"},
    {"title": "Strategy and Performance Alignment (Part 2)", "type": "embed", "vimeo": "416547902"},
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
            "order": 1 + i
        })
        print(f"  [{1+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {1 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
