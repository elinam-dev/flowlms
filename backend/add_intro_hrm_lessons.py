import asyncio, os, uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE = "http://localhost:8000/uploads/images/HR/introduction_to_modern_human_resource_management"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/introduction_to_modern_hrm{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

lessons_data = [
    {"title": f"Introduction to Modern HRM - Slide {i}", "type": "text", "content": img(i)}
    for i in range(1, 139)
]

async def main():
    course = await db.courses.find_one({"id": "d75e50b0-1ac4-4af3-aefd-31fbefad09ff"})
    print(f"Course: {course['title']}")
    module = await db.modules.find_one({"course_id": course["id"]})
    await db.lessons.delete_many({"module_id": module["id"]})
    for i, lesson in enumerate(lessons_data):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson["title"],
            "content_type": lesson["type"],
            "content": lesson["content"],
            "duration_minutes": 10,
            "order": i
        })
    print(f"Added {len(lessons_data)} lessons")

asyncio.run(main())
