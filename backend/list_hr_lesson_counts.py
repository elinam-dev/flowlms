import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

async def main():
    courses = await db.courses.find({'category': 'hr'}, {'_id': 0, 'id': 1, 'title': 1}).to_list(100)
    for c in courses:
        modules = await db.modules.find({'course_id': c['id']}, {'_id': 0, 'id': 1}).to_list(100)
        lesson_count = 0
        for m in modules:
            count = await db.lessons.count_documents({'module_id': m['id']})
            lesson_count += count
        print(f"{lesson_count} lesson(s) - {c['title']}")

asyncio.run(main())
