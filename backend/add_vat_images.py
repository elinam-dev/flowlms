import asyncio, os, uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE = "http://localhost:8000/uploads/images/Finance/basics_of_value-added_tax"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/basics_of_value-added_tax{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

async def main():
    course = await db.courses.find_one({"id": "7cc7787d-8050-4432-a5ae-6fc22664fe18"})
    module = await db.modules.find_one({"course_id": course["id"]})
    count = await db.lessons.count_documents({"module_id": module["id"]})

    for i, n in enumerate(range(2, 9)):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": f"Basics of Value-Added Tax - Slide {n}",
            "content_type": "text",
            "content": img(n),
            "duration_minutes": 10,
            "order": count + i
        })

    print(f"Added 7 image lessons. Total: {count + 7}")

asyncio.run(main())
