"""
List all courses and check for missing quizzes
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def list_courses_and_quizzes():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    courses = await db.courses.find({}).sort("code", 1).to_list(None)
    print(f"Total courses: {len(courses)}\n")
    
    missing = []
    
    for course in courses:
        module = await db.modules.find_one({"course_id": course['id']})
        if module:
            quiz = await db.quizzes.find_one({"module_id": module['id']})
            status = "✓" if quiz else "✗ MISSING"
            if not quiz:
                missing.append(course['title'])
            print(f"{status} {course.get('code', 'N/A'):15} {course['title']}")
    
    print(f"\n{'='*60}")
    print(f"Courses missing quizzes: {len(missing)}")
    if missing:
        print("\nMissing quiz courses:")
        for title in missing:
            print(f"  - {title}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(list_courses_and_quizzes())
