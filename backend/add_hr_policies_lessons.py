#!/usr/bin/env python3
"""
Add lessons to Human Resource policies and organization structure course
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
    {
        "title": "Human Resource Policies Overview",
        "type": "image",
        "content": f"{BASE_URL}/uploads/images/HR/human_resource_policies/human_resource_policies01.jpeg"
    },
    {
        "title": "Human Resource",
        "type": "embed",
        "content": "https://player.vimeo.com/video/911776520?quality=720p&audiotrack=main&texttrack=en"
    },
    {
        "title": "Essential Human Resource Systems",
        "type": "embed",
        "content": "https://player.vimeo.com/video/911776527?quality=720p&audiotrack=main&texttrack=en"
    },
    {
        "title": "Organization Structure and Reporting Relationships",
        "type": "embed",
        "content": "https://player.vimeo.com/video/911776533?quality=720p&audiotrack=main&texttrack=en"
    },
    {
        "title": "Designing Organizational Structure",
        "type": "embed",
        "content": "https://player.vimeo.com/video/911776541?quality=720p&audiotrack=main&texttrack=en"
    },
    {
        "title": "Bands and Grades",
        "type": "embed",
        "content": "https://player.vimeo.com/video/911776550?quality=720p&audiotrack=main&texttrack=en"
    },
    {
        "title": "Designing Bands and Grades Structure",
        "type": "embed",
        "content": "https://player.vimeo.com/video/911776557?quality=720p&audiotrack=main&texttrack=en"
    },
    {
        "title": "Need for Human Resource Policies",
        "type": "embed",
        "content": "https://player.vimeo.com/video/911776565?quality=720p&audiotrack=main&texttrack=en"
    },
    {
        "title": "Setting up Your Company's Policy Framework",
        "type": "embed",
        "content": "https://player.vimeo.com/video/911776576?quality=720p&audiotrack=main&texttrack=en"
    },
    {
        "title": "HR Policies Diagram 2",
        "type": "image",
        "content": f"{BASE_URL}/uploads/images/HR/human_resource_policies/human_resource_policies02.jpeg"
    },
    {
        "title": "HR Policies Diagram 3",
        "type": "image",
        "content": f"{BASE_URL}/uploads/images/HR/human_resource_policies/human_resource_policies03.jpeg"
    },
    {
        "title": "HR Policies Diagram 4",
        "type": "image",
        "content": f"{BASE_URL}/uploads/images/HR/human_resource_policies/human_resource_policies04.jpeg"
    },
]

def make_content(lesson):
    if lesson["type"] == "image":
        return f'<div style="text-align: center; padding: 20px;"><img src="{lesson["content"]}" alt="{lesson["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
    else:
        return f'<div style="text-align: center;"><iframe src="{lesson["content"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'

async def add_lessons():
    course = await db.courses.find_one(
        {"title": {"$regex": "human resource policies", "$options": "i"}},
        {"_id": 0}
    )
    if not course:
        print("Course not found!")
        return

    print(f"Found: {course['title']}")

    # Get or create module
    module = await db.modules.find_one({"course_id": course["id"]})
    if not module:
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course["id"],
            "title": "Course Content",
            "description": "Human Resource Policies and Organization Structure",
            "order": 0
        })
        module = await db.modules.find_one({"id": module_id})
        print("Created module")
    else:
        # Clear existing lessons
        await db.lessons.delete_many({"module_id": module["id"]})
        print(f"Cleared existing lessons from module: {module['title']}")

    # Add lessons
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

    # Publish the course
    await db.courses.update_one(
        {"id": course["id"]},
        {"$set": {"is_published": True}}
    )
    print(f"\nAdded {len(LESSONS)} lessons and published the course.")

if __name__ == "__main__":
    asyncio.run(add_lessons())
