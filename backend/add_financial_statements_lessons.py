import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

BASE = "http://localhost:8000/uploads/images/Finance/financial_statements"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/financial_statements{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

lessons_data = [
    {"title": f"Financial Statement Analysis - Slide {i}", "type": "text", "content": img(i)}
    for i in range(1, 50)
]

async def add_lessons():
    course = await db.courses.find_one({"title": {"$regex": "financial statement analysis", "$options": "i"}})
    print(f"Course: {course['title']}")

    module = await db.modules.find_one({"course_id": course['id']})

    await db.lessons.delete_many({"module_id": module['id']})

    for i, lesson in enumerate(lessons_data):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module['id'],
            "title": lesson['title'],
            "content_type": lesson['type'],
            "content": lesson['content'],
            "duration_minutes": 10,
            "order": i
        })

    print(f"Added {len(lessons_data)} lessons")

if __name__ == "__main__":
    asyncio.run(add_lessons())
