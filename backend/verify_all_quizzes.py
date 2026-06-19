import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def verify_quizzes():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    courses = await db.courses.find({}).sort("title", 1).to_list(None)
    quizzes_count = await db.quizzes.count_documents({})
    
    print(f"Total courses: {len(courses)}")
    print(f"Total quizzes: {quizzes_count}")
    
    missing = []
    for course in courses:
        module = await db.modules.find_one({"course_id": course['id']})
        if module:
            quiz = await db.quizzes.find_one({"module_id": module['id']})
            if not quiz:
                missing.append(course['title'])
    
    if missing:
        print(f"\nCourses without quizzes: {len(missing)}")
        for title in missing:
            print(f"  - {title}")
    else:
        print("\nAll courses have quizzes!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(verify_quizzes())
