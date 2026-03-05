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

async def add_b2b_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "b2b.*supply.*chain", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    # Update first lesson with first image
    lesson1 = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Introduction"
    })
    
    if lesson1:
        content = f'<div style="text-align: center; padding: 20px;"><img src="/uploads/images/B2B-supply-chain-management/b2bsupply1.jpeg" alt="Introduction" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        await db.lessons.update_one(
            {"id": lesson1["id"]},
            {"$set": {"content": content, "content_type": "text"}}
        )
        print(f"Updated: Introduction with b2bsupply1.jpeg")
    
    # Add remaining 40 images
    for i in range(2, 42):
        content = f'<div style="text-align: center; padding: 20px;"><img src="/uploads/images/B2B-supply-chain-management/b2bsupply{i}.jpeg" alt="B2B Supply Chain - Part {i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": f"B2B Supply Chain - Part {i}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 5,
            "order": i - 1
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"Added: B2B Supply Chain - Part {i}")
    
    print(f"\nDone! Added 41 image lessons")

if __name__ == "__main__":
    asyncio.run(add_b2b_lessons())
