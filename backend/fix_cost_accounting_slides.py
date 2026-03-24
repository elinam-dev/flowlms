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

BASE = "http://localhost:8000/uploads/images/Finance/diploma_in_cost_accounting"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/diploma_in_cost_accounting{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

async def fix():
    module = await db.modules.find_one({"course_id": "3e5143d8-e3ff-489a-a728-81d059b85787"})

    # Find "Cash Budget for the First Six Months" lesson order
    cash_lesson = await db.lessons.find_one({"module_id": module['id'], "title": "Cash Budget for the First Six Months"})
    insert_after = cash_lesson['order']  # order = 39

    # Shift all lessons after that point by 2
    lessons_to_shift = await db.lessons.find({
        "module_id": module['id'],
        "order": {"$gt": insert_after}
    }).to_list(100)

    for lesson in lessons_to_shift:
        await db.lessons.update_one(
            {"id": lesson['id']},
            {"$set": {"order": lesson['order'] + 2}}
        )

    # Insert slide 8 and slide 9
    await db.lessons.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module['id'],
        "title": "Diploma in Cost Accounting - Slide 8",
        "content_type": "text",
        "content": img(8),
        "duration_minutes": 5,
        "order": insert_after + 1
    })

    await db.lessons.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module['id'],
        "title": "Diploma in Cost Accounting - Slide 9",
        "content_type": "text",
        "content": img(9),
        "duration_minutes": 5,
        "order": insert_after + 2
    })

    total = await db.lessons.count_documents({"module_id": module['id']})
    print(f"Inserted slides 8 and 9 after '{cash_lesson['title']}'")
    print(f"Total lessons now: {total}")

if __name__ == "__main__":
    asyncio.run(fix())
