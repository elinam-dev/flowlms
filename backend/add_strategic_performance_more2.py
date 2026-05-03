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
    {"title": "Strategic Performance Diagram 5", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_005.jpeg"},
    {"title": "Strategic Performance Diagram 6", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_006.jpeg"},
    {"title": "Strategic Performance Diagram 7", "type": "image", "url": f"{BASE_URL}/uploads/images/HR/strategic_performance_management/strategic_performance_007.jpeg"},
    {"title": "Performance (Determinants & Factors)", "type": "embed", "vimeo": "416548652"},
    {"title": "Dimensions of Performance (Task & Context)", "type": "embed", "vimeo": "416549247"},
    {"title": "Behavior Approach", "type": "embed", "vimeo": "416551347"},
    {"title": "Result and Trait Approach", "type": "embed", "vimeo": "416550142"},
    {"title": "Measuring Results, Determining Accountability & Examples", "type": "embed", "vimeo": "416552172"},
    {"title": "Determining Performance Standards & Examples", "type": "embed", "vimeo": "416551854"},
    {"title": "Measuring Behaviour (Competencies)", "type": "embed", "vimeo": "416552062"},
    {"title": "Measurement System (Comparative)", "type": "embed", "vimeo": "416657670"},
    {"title": "Measurement System (Absolute)", "type": "embed", "vimeo": "416656459"},
    {"title": "Components & Characteristics of an Appraisal Form", "type": "embed", "vimeo": "416660320"},
    {"title": "Determining Overall Rating, who should Provide PMI & Common Problems", "type": "embed", "vimeo": "416662367"},
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
            "order": 25 + i
        })
        print(f"  [{25+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {25 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
