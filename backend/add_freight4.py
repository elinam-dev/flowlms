#!/usr/bin/env python3
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

async def add_freight4():
    course = await db.courses.find_one({
        "title": {"$regex": "freight.*broker.*training", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    content = '<div style="text-align: center; padding: 20px;"><img src="/uploads/images/freight/freight4.jpeg" alt="Freight Broker Diagram 3" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
    
    lesson_doc = {
        "id": str(uuid.uuid4()),
        "module_id": module["id"],
        "title": "Freight Broker Diagram 3",
        "content_type": "text",
        "content": content,
        "duration_minutes": 5,
        "order": 28
    }
    
    await db.lessons.insert_one(lesson_doc)
    print("Added: Freight Broker Diagram 3")

if __name__ == "__main__":
    asyncio.run(add_freight4())
