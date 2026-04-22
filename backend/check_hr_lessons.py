import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

async def main():
    courses = await db.courses.find(
        {"category": {"$regex": "hr|human resource|HR Policy", "$options": "i"}},
        {"_id": 0, "id": 1, "title": 1}
    ).to_list(200)

    print(f"{'Course Title':<65} {'Modules':>7} {'Lessons':>7}")
    print("-" * 82)

    for c in courses:
        modules = await db.modules.find({"course_id": c["id"]}, {"_id": 0, "id": 1}).to_list(100)
        lesson_count = 0
        for m in modules:
            lessons = await db.lessons.count_documents({"module_id": m["id"]})
            lesson_count += lessons

        flag = "" if lesson_count > 1 else "  << empty"
        title = c['title'][:64]
        print(f"{title:<65} {len(modules):>7} {lesson_count:>7}{flag}")

asyncio.run(main())
