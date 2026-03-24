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

async def find():
    course = await db.courses.find_one({"title": {"$regex": "accounting cycle", "$options": "i"}})
    if course:
        print(f"Found: {course['title']}")
        print(f"Course ID: {course['id']}")
        print(f"Category: {course.get('category', 'N/A')}")
        print(f"Published: {course.get('is_published', False)}")

        modules = await db.modules.find({"course_id": course['id']}).to_list(10)
        print(f"\nModules: {len(modules)}")
        for module in modules:
            lessons = await db.lessons.count_documents({"module_id": module['id']})
            print(f"  - {module['title']}: {lessons} lessons")
    else:
        print("Course not found")

if __name__ == "__main__":
    asyncio.run(find())
