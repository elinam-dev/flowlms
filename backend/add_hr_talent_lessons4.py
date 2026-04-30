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

LESSONS = [
    {"title": "Module 4 - Getting Started", "vimeo": "880310771"},
    {"title": "Access the Module Manual", "vimeo": "899884186"},
    {"title": "Onboarding Purpose", "vimeo": "880311795"},
    {"title": "Case Study: Onboarding Strategy", "vimeo": "880311839"},
    {"title": "Onboarding Overview", "vimeo": "880311887"},
    {"title": "Case Study: Onboarding Overview", "vimeo": "880311908"},
    {"title": "Preparing for Onboarding", "vimeo": "880313152"},
    {"title": "Case Study: Preparations", "vimeo": "880313184"},
    {"title": "Onboarding Millennials", "vimeo": "880313287"},
    {"title": "Case Study: Onboarding Millennials", "vimeo": "880313328"},
    {"title": "Onboarding Checklist", "vimeo": "880314598"},
    {"title": "Case Study: Onboarding Checklist", "vimeo": "880314656"},
    {"title": "Checklist for Millennials", "vimeo": "880314719"},
    {"title": "Case Study: Millennials Checklist", "vimeo": "880314779"},
    {"title": "Developing the Onboarding Program", "vimeo": "880316299"},
    {"title": "Case Study: Developing a Program", "vimeo": "880316339"},
    {"title": "Engaging Millennials", "vimeo": "880316437"},
    {"title": "Case Study: Engaging Millennials", "vimeo": "880316589"},
    {"title": "Post-Onboarding Support", "vimeo": "880318034"},
    {"title": "Case Study: Post-Onboarding", "vimeo": "880318111"},
    {"title": "Post-Onboarding for Millennials", "vimeo": "880318185"},
    {"title": "Case Study: Millennials' Post-Onboarding", "vimeo": "880318216"},
    {"title": "Setting Expectations", "vimeo": "880320378"},
    {"title": "Millennials Expectations", "vimeo": "880320551"},
    {"title": "Case Study: Millennials' Expectations", "vimeo": "880320594"},
    {"title": "Resiliency and Flexibility", "vimeo": "880320135"},
    {"title": "Case Study: Resiliency & Flexibility", "vimeo": "880320278"},
    {"title": "Mentoring Millennials", "vimeo": "919769483"},
]

def make_content(vimeo_id):
    return f'<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/{vimeo_id}?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

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
            "content_type": "embed",
            "content": make_content(lesson["vimeo"]),
            "duration_minutes": 10,
            "order": 66 + i
        })
        print(f"  [{66+i}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course now has {66 + len(LESSONS)} total lessons.")

if __name__ == "__main__":
    asyncio.run(add())
