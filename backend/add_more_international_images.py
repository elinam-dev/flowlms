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

IMAGES = [
    "/uploads/images/international_marketing__and_supply_chain_management/internationalmarketing2.jpeg",
    "/uploads/images/international_marketing__and_supply_chain_management/internationalmarketing3.jpeg",
    "/uploads/images/international_marketing__and_supply_chain_management/internationalmarketing4.jpeg"
]

async def add_more_images():
    course = await db.courses.find_one({
        "title": {"$regex": "international.*marketing.*supply.*chain", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    for i, img_path in enumerate(IMAGES, start=2):
        content = f'<div style="text-align: center; padding: 20px;"><img src="{img_path}" alt="International Marketing Diagram {i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": f"International Marketing Diagram {i}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 5,
            "order": 10 + i
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"Added: International Marketing Diagram {i}")
    
    print(f"\nAdded {len(IMAGES)} images")

if __name__ == "__main__":
    asyncio.run(add_more_images())
