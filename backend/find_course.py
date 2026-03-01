#!/usr/bin/env python3
"""
Script to find Diploma in Supply Chain Management course
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

async def find_course():
    """Find the Diploma in Supply Chain Management course"""
    
    # Search for the course
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    if course:
        print("Course Found!")
        print(f"\nTitle: {course['title']}")
        print(f"ID: {course['id']}")
        print(f"Category: {course.get('category', 'N/A')}")
        print(f"Description: {course.get('description', 'N/A')}")
        print(f"Duration: {course.get('duration_hours', 'N/A')} hours")
        
        # Find modules
        print("\n--- Modules ---")
        modules = await db.modules.find({"course_id": course["id"]}).to_list(None)
        if modules:
            for mod in modules:
                print(f"  • {mod['title']} (ID: {mod['id']})")
                
                # Find lessons in this module
                lessons = await db.lessons.find({"module_id": mod["id"]}).to_list(None)
                if lessons:
                    print(f"    Lessons: {len(lessons)}")
                    for lesson in lessons:
                        print(f"      - {lesson['title']} ({lesson.get('content_type', 'N/A')})")
        else:
            print("  No modules found")
    else:
        print("Course not found!")
        print("\nSearching all courses with 'supply' in title:")
        async for c in db.courses.find({"title": {"$regex": "supply", "$options": "i"}}):
            print(f"  - {c['title']}")

if __name__ == "__main__":
    asyncio.run(find_course())
