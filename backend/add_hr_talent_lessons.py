#!/usr/bin/env python3
"""
Add lessons to HR: Talent Management and Workforce Development
"""
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
    {"title": "HR Talent Overview", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent01.jpeg"},
    {"title": "Diploma Course Overview", "type": "embed", "content": "https://player.vimeo.com/video/879161169?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Module 1 Getting Started", "type": "embed", "content": "https://player.vimeo.com/video/878993711?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Access the Module Manual", "type": "embed", "content": "https://player.vimeo.com/video/899892055?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Human Resources Concept Today", "type": "embed", "content": "https://player.vimeo.com/video/879000839?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: HR Concept Today", "type": "embed", "content": "https://player.vimeo.com/video/879003674?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Interviewing Techniques", "type": "embed", "content": "https://player.vimeo.com/video/879001175?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Interview Techniques", "type": "embed", "content": "https://player.vimeo.com/video/879000745?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Orientation and Retention", "type": "embed", "content": "https://player.vimeo.com/video/879006356?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Orientation and Retention", "type": "embed", "content": "https://player.vimeo.com/video/879006059?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Following Up With New Employees", "type": "embed", "content": "https://player.vimeo.com/video/879005847?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Following Up", "type": "embed", "content": "https://player.vimeo.com/video/879007918?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Workplace Health and Safety", "type": "embed", "content": "https://player.vimeo.com/video/879006361?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Health and Safety", "type": "embed", "content": "https://player.vimeo.com/video/879006201?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Bullying, Harassment and Violence", "type": "embed", "content": "https://player.vimeo.com/video/879011201?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Promoting Workplace Wellness", "type": "embed", "content": "https://player.vimeo.com/video/879012496?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Promoting Wellness", "type": "embed", "content": "https://player.vimeo.com/video/879011673?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Feedback Matters", "type": "embed", "content": "https://player.vimeo.com/video/879014416?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Feedback", "type": "embed", "content": "https://player.vimeo.com/video/879011980?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Disciplining an Employee", "type": "embed", "content": "https://player.vimeo.com/video/879017340?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Disciplining", "type": "embed", "content": "https://player.vimeo.com/video/879015333?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Terminating an Employee", "type": "embed", "content": "https://player.vimeo.com/video/879017058?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Termination", "type": "embed", "content": "https://player.vimeo.com/video/879016088?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Module 1 Wrapping Up", "type": "embed", "content": "https://player.vimeo.com/video/879014032?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "HR Talent Diagram 2", "type": "image", "content": f"{BASE_URL}/uploads/images/HR/hr_talent/hr_talent02.jpeg"},
]

def make_content(lesson):
    if lesson["type"] == "image":
        return f'<div style="text-align: center; padding: 20px;"><img src="{lesson["content"]}" alt="{lesson["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
    else:
        return f'<div style="text-align: center;"><iframe src="{lesson["content"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def add_lessons():
    course = await db.courses.find_one(
        {"title": {"$regex": "talent management and workforce", "$options": "i"}},
        {"_id": 0}
    )
    if not course:
        print("Course not found!")
        return
    print(f"Found: {course['title']}")

    module = await db.modules.find_one({"course_id": course["id"]})
    if not module:
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course["id"],
            "title": "Course Content",
            "order": 0
        })
        module = await db.modules.find_one({"id": module_id})
    else:
        await db.lessons.delete_many({"module_id": module["id"]})
        print("Cleared existing lessons")

    for i, lesson in enumerate(LESSONS):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson["title"],
            "content_type": "text" if lesson["type"] == "image" else "embed",
            "content": make_content(lesson),
            "duration_minutes": 5 if lesson["type"] == "image" else 10,
            "order": i
        })
        print(f"  [{i+1}] {lesson['title']}")

    print(f"\nAdded {len(LESSONS)} lessons. Course NOT published yet — more content to come.")

if __name__ == "__main__":
    asyncio.run(add_lessons())
