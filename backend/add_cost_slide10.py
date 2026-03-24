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

async def add():
    module = await db.modules.find_one({"course_id": "3e5143d8-e3ff-489a-a728-81d059b85787"})
    
    # Get last lesson order
    last_lesson = await db.lessons.find_one({"module_id": module['id']}, sort=[("order", -1)])
    
    await db.lessons.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module['id'],
        "title": "Diploma in Cost Accounting - Slide 10",
        "content_type": "text",
        "content": '<div style="text-align: center;"><img src="http://localhost:8000/uploads/images/Finance/diploma_in_cost_accounting/diploma_in_cost_accounting10.jpeg" alt="Slide 10" style="max-width: 100%; height: auto;" /></div>',
        "duration_minutes": 5,
        "order": last_lesson['order'] + 1
    })
    
    total = await db.lessons.count_documents({"module_id": module['id']})
    print(f"Added slide 10. Total lessons: {total}")

if __name__ == "__main__":
    asyncio.run(add())
