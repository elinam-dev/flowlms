import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

async def main():
    course = await db.courses.find_one(
        {"title": {"$regex": "HR Analytics", "$options": "i"}},
        {"_id": 0}
    )
    print("Course:", course)
    
    modules = await db.modules.find({"course_id": course["id"]}, {"_id": 0}).to_list(100)
    for m in modules:
        print("\nModule:", m)
        lessons = await db.lessons.find({"module_id": m["id"]}, {"_id": 0}).to_list(100)
        for l in lessons:
            print("  Lesson:", l)

asyncio.run(main())
