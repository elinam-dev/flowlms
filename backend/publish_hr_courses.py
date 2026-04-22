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

    to_publish = []
    empty = []

    for c in courses:
        modules = await db.modules.find({"course_id": c["id"]}, {"_id": 0, "id": 1}).to_list(100)
        lesson_count = 0
        for m in modules:
            lesson_count += await db.lessons.count_documents({"module_id": m["id"]})
        
        if lesson_count > 1:
            to_publish.append(c)
        else:
            empty.append(c)

    print("Publishing courses with content:")
    for c in to_publish:
        await db.courses.update_one({"id": c["id"]}, {"$set": {"published": True}})
        print(f"  [PUBLISHED] {c['title']}")

    print(f"\nEmpty courses ({len(empty)}) - not published:")
    for c in empty:
        print(f"  - {c['title']}")

asyncio.run(main())
