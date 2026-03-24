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

async def add_accounting_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "fundamentals.*accounting", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    # Update first lesson with first image
    lesson1 = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Introduction"
    })
    
    if lesson1:
        content = '<div style="text-align: center; padding: 20px;"><img src="/uploads/images/Finance/fundamentals_of_accounting/fundamentals_of_accounting1.jpeg" alt="Introduction" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        await db.lessons.update_one(
            {"id": lesson1["id"]},
            {"$set": {"content": content, "content_type": "text"}}
        )
        print(f"Updated: Introduction")
    
    # Add remaining 173 images
    for i in range(2, 175):
        content = f'<div style="text-align: center; padding: 20px;"><img src="/uploads/images/Finance/fundamentals_of_accounting/fundamentals_of_accounting{i}.jpeg" alt="Fundamentals of Accounting - Part {i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": f"Fundamentals of Accounting - Part {i}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 5,
            "order": i - 1
        }
        
        await db.lessons.insert_one(lesson_doc)
        if i % 20 == 0:
            print(f"Added {i-1} lessons...")
    
    print(f"\nDone! Added 174 image lessons")

if __name__ == "__main__":
    asyncio.run(add_accounting_lessons())
