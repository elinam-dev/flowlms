#!/usr/bin/env python3
"""
Script to add Supply Chain Networks lesson with Vimeo embed
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def add_supply_chain_lesson():
    """Add Supply Chain Networks lesson with Vimeo embed"""
    
    # Find the course
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    if not course:
        print("Course not found")
        return
    
    # Find or create a module
    module = await db.modules.find_one({"course_id": course["id"]})
    
    if not module:
        # Create a module
        module_id = str(uuid.uuid4())
        module_doc = {
            "id": module_id,
            "course_id": course["id"],
            "title": "Course Content",
            "description": "Supply Chain Management Lessons",
            "order": 0
        }
        await db.modules.insert_one(module_doc)
        module = module_doc
    
    # Create the lesson
    lesson_id = str(uuid.uuid4())
    lesson_doc = {
        "id": lesson_id,
        "module_id": module["id"],
        "title": "Supply Chain Networks",
        "content_type": "embed",
        "content": '<iframe src="https://player.vimeo.com/video/95264460?quality=720p&amp;audiotrack=main&amp;texttrack=en" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>',
        "duration_minutes": 10,
        "order": 0
    }
    
    await db.lessons.insert_one(lesson_doc)
    print(f"Added lesson: {lesson_doc['title']}")
    print(f"Course: {course['title']}")

if __name__ == "__main__":
    asyncio.run(add_supply_chain_lesson())