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

async def add_images():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    # Add image after Module 1.2
    module1 = await db.modules.find_one({
        "course_id": course["id"],
        "title": {"$regex": "Module 1.*Global Supply Chain"}
    })
    
    if module1:
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module1["id"],
            "title": "Supply Chain Architecture Diagram",
            "content_type": "image",
            "content": r"C:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\diploma in supply chain\supplychain2.jpg",
            "duration_minutes": 5,
            "order": 2
        }
        await db.lessons.insert_one(lesson_doc)
        print("Added image after Module 1.2")
    
    # Add image after Module 2
    module2 = await db.modules.find_one({
        "course_id": course["id"],
        "title": {"$regex": "Module 2.*Strategic Procurement"}
    })
    
    if module2:
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module2["id"],
            "title": "Procurement Strategy Visual",
            "content_type": "image",
            "content": r"C:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\diploma in supply chain\supplychain3.jpg",
            "duration_minutes": 5,
            "order": 2
        }
        await db.lessons.insert_one(lesson_doc)
        print("Added image after Module 2")

if __name__ == "__main__":
    asyncio.run(add_images())
