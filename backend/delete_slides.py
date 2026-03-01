#!/usr/bin/env python3
"""
Script to delete slide lessons from Diploma in Supply Chain Management course
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def delete_slides():
    """Delete slide lessons from the course"""
    
    # Find the course
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    if not course:
        print("Course not found!")
        return
    
    print(f"Found course: {course['title']}")
    
    # Find all modules for this course
    modules = await db.modules.find({"course_id": course["id"]}).to_list(None)
    
    deleted_count = 0
    for module in modules:
        # Find and delete slide lessons
        lessons = await db.lessons.find({"module_id": module["id"]}).to_list(None)
        
        for lesson in lessons:
            if lesson.get("content_type") == "slides":
                await db.lessons.delete_one({"id": lesson["id"]})
                print(f"Deleted: {lesson['title']}")
                deleted_count += 1
    
    print(f"\nDeleted {deleted_count} slide lesson(s)")

if __name__ == "__main__":
    asyncio.run(delete_slides())
