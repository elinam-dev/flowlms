import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def fix():
    courses = await db.courses.find({}, {"_id": 0, "id": 1, "title": 1}).to_list(None)
    unpublished = []

    for course in courses:
        modules = await db.modules.find({"course_id": course["id"]}, {"_id": 0, "id": 1}).to_list(None)
        module_ids = [m["id"] for m in modules]
        lesson_count = await db.lessons.count_documents({"module_id": {"$in": module_ids}}) if module_ids else 0

        if lesson_count <= 1:
            unpublished.append(course["title"])
            await db.courses.update_one({"id": course["id"]}, {"$set": {"is_published": False}})

    print(f"Unpublished {len(unpublished)} courses:")
    for t in unpublished:
        print(f"  - {t}")
    print("Done.")
    client.close()

asyncio.run(fix())
