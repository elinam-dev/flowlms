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
    {"title": "Performance Analysis (Concept, Objectives & Methodology)", "type": "embed", "vimeo": "416846112"},
    {"title": "Performance Analysis Quadrant", "type": "embed", "vimeo": "416843089"},
    {"title": "PMS Data and Examples", "type": "embed", "vimeo": "416847968"},
    {"title": "Use of Appraisal Data", "type": "embed", "vimeo": "416850472"},
    {"title": "Strategic Performance Diagram 16", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_016.jpeg"},
    {"title": "Strategic Performance Diagram 17", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_017.jpeg"},
    {"title": "Strategic Performance Diagram 18", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_018.jpeg"},
    {"title": "Potential Appraisal", "type": "embed", "vimeo": "416853851"},
    {"title": "Purpose/Need for Potential Appraisal", "type": "embed", "vimeo": "416881358"},
    {"title": "Performance Vs Potential Matrix & Techniques Used", "type": "embed", "vimeo": "417068305"},
    {"title": "Potential Appraisal & Leaderless Group Discussion", "type": "embed", "vimeo": "417070498"},
    {"title": "Reward System (Traditional Approach)", "type": "embed", "vimeo": "417079176"},
    {"title": "Contingent Pay Plans & Types and Role of Rewards", "type": "embed", "vimeo": "417073257"},
    {"title": "Linking Performance Measurement and Compensation", "type": "embed", "vimeo": "417242803"},
    {"title": "Designing a Pay-For-Performance Plan", "type": "embed", "vimeo": "417235114"},
    {"title": "Different Types of Variable Pay Plans", "type": "embed", "vimeo": "417240964"},
    {"title": "Performance Management and the Law", "type": "embed", "vimeo": "417245302"},
    {"title": "Legal Principles Affecting Performance Management", "type": "embed", "vimeo": "417243635"},
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
            "order": 78 + i
        })
        print(f"  [{78+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {78 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
