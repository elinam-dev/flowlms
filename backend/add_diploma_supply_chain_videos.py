#!/usr/bin/env python3
"""
Script to add video lessons to Diploma in Supply Chain Management course
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

# List of video lessons to add
VIDEO_LESSONS = [
    {
        "title": "Integrated Supply Chain Network",
        "vimeo_id": "95265089",
        "duration_minutes": 15
    },
    {
        "title": "Best Practices in SCN-1",
        "vimeo_id": "95265721",
        "duration_minutes": 12
    },
    {
        "title": "The Great Trade Collapse",
        "vimeo_id": "95267682",
        "duration_minutes": 10
    },
    {
        "title": "Supply Chain Strategy",
        "vimeo_id": "95268164",
        "duration_minutes": 10
    },
    {
        "title": "Business Model",
        "vimeo_id": "95269176",
        "duration_minutes": 12
    },
    {
        "title": "ZARA",
        "vimeo_id": "95270183",
        "duration_minutes": 10
    }
]

def create_embed_content(vimeo_id):
    """Create Vimeo embed HTML"""
    return f'<iframe src="https://player.vimeo.com/video/{vimeo_id}?quality=720p&audiotrack=main&texttrack=en" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>'

async def add_video_lessons():
    """Add all video lessons to the Diploma in Supply Chain Management course"""
    
    # Find the course
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    if not course:
        print("Course 'Diploma in Supply Chain Management' not found!")
        print("Available courses:")
        async for c in db.courses.find({"category": "SUPPLY CHAIN"}):
            print(f"  - {c['title']}")
        return
    
    print(f"Found course: {course['title']}")
    print(f"Course ID: {course['id']}")
    
    # Find or create a module for video lessons
    module = await db.modules.find_one({
        "course_id": course["id"],
        "title": "Video Lessons"
    })
    
    if not module:
        # Create a new module for videos
        module_id = str(uuid.uuid4())
        module_doc = {
            "id": module_id,
            "course_id": course["id"],
            "title": "Video Lessons",
            "description": "Video lessons for Diploma in Supply Chain Management",
            "order": 1  # Put it after the first module
        }
        await db.modules.insert_one(module_doc)
        module = module_doc
        print(f"Created new module: {module['title']}")
    else:
        print(f"Using existing module: {module['title']}")
    
    # Get existing lessons count to determine order
    existing_lessons = await db.lessons.count_documents({"module_id": module["id"]})
    start_order = existing_lessons
    
    # Add each video lesson
    added_count = 0
    for i, video in enumerate(VIDEO_LESSONS):
        lesson_id = str(uuid.uuid4())
        lesson_doc = {
            "id": lesson_id,
            "module_id": module["id"],
            "title": video["title"],
            "content_type": "embed",
            "content": create_embed_content(video["vimeo_id"]),
            "duration_minutes": video["duration_minutes"],
            "order": start_order + i
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"  Added: {video['title']} (Vimeo: {video['vimeo_id']})")
        added_count += 1
    
    print(f"\nSuccessfully added {added_count} video lessons to '{course['title']}'")
    print(f"Module: {module['title']}")

if __name__ == "__main__":
    asyncio.run(add_video_lessons())
