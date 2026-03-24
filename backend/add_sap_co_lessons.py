import asyncio, os, uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

FOLDER = r"c:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\Finance\essentials_of_sap"
BASE = "http://localhost:8000/uploads/images/Finance/essentials_of_sap"

# Rename
screenshots = sorted([f for f in os.listdir(FOLDER) if f.startswith('Screenshot')])
for i, f in enumerate(screenshots, start=1):
    os.rename(os.path.join(FOLDER, f), os.path.join(FOLDER, f'essentials_of_sap{i}.jpeg'))
print(f'Renamed {len(screenshots)} files')

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/essentials_of_sap{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

lessons_data = [
    {"title": f"Essentials of SAP CO - Slide {i}", "type": "text", "content": img(i)}
    for i in range(1, len(screenshots) + 1)
]

async def add_lessons():
    course = await db.courses.find_one({"id": "afaae2d2-241d-4a23-b08e-c8abf640ca56"})
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

asyncio.run(add_lessons())
