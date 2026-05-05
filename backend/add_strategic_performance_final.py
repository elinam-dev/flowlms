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
    {"title": "Strategic Performance Diagram 19", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_019.jpeg"},
    {"title": "Strategic Performance Diagram 20", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_020.jpeg"},
    {"title": "Strategic Performance Diagram 21", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_021.jpeg"},
    {"title": "PMS in India (PWC Survey Report)", "type": "embed", "vimeo": "417248522"},
    {"title": "Factors Impeding the Effectiveness of PMS", "type": "embed", "vimeo": "417247841"},
    {"title": "The Role of Organizational Culture in PM", "type": "embed", "vimeo": "417250198"},
    {"title": "Cultural Dimensions, Descriptions and PM Implications", "type": "embed", "vimeo": "417248978"},
    {"title": "Technology and Performance Management", "type": "embed", "vimeo": "417251955"},
    {"title": "Role of Technology in PM", "type": "embed", "vimeo": "417251202"},
    {"title": "PMS in Select Indian Companies (Part 1)", "type": "embed", "vimeo": "417253088"},
    {"title": "PMS in Select Indian Companies (Part 2)", "type": "embed", "vimeo": "417254291"},
    {"title": "Changes in the Workplace", "type": "embed", "vimeo": "417256013"},
    {"title": "On going Evaluation and Feedback System", "type": "embed", "vimeo": "417257025"},
    {"title": "Strategic Performance Diagram 22", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_022.jpeg"},
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
            "order": 96 + i
        })
        print(f"  [{96+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {96 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
