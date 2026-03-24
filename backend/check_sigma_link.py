import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def check():
    # Find a learn_sigma_six lesson
    lesson = await db.lessons.find_one({"content": {"$regex": "learn_sigma_six1"}})
    if lesson:
        print(f"Lesson: {lesson.get('title', 'No title')}")
        print(f"Module ID: {lesson.get('module_id', 'No module')}")
        
        # Find module
        if lesson.get('module_id'):
            module = await db.modules.find_one({"id": lesson['module_id']})
            if module:
                print(f"Module: {module['title']}")
                print(f"Course ID: {module['course_id']}")
                
                # Find course
                course = await db.courses.find_one({"id": module['course_id']})
                if course:
                    print(f"Current Course: {course['title']}")
    else:
        print("No lesson found")
    
    # Find the correct course
    correct_course = await db.courses.find_one({"title": {"$regex": "Learn six sigma", "$options": "i"}})
    if correct_course:
        print(f"\nCorrect Course: {correct_course['title']}")
        print(f"Correct Course ID: {correct_course['id']}")

if __name__ == "__main__":
    asyncio.run(check())
