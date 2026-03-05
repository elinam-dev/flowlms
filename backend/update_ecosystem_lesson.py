#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def update_ecosystem_lesson():
    course = await db.courses.find_one({
        "title": {"$regex": "understanding.*supply.*chain.*ecosystem", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    lesson = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Introduction"
    })
    
    if lesson:
        content = '<div style="text-align: center; padding: 20px;"><img src="/uploads/images/understanding_supply_chain_ecosystem_fundamentals_of_using_six_sigma_in_supply_chain/ecosystem1.jpeg" alt="Introduction" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        await db.lessons.update_one(
            {"id": lesson["id"]},
            {"$set": {"content": content, "content_type": "text"}}
        )
        print(f"Updated: {lesson['title']} with ecosystem1.jpeg")

if __name__ == "__main__":
    asyncio.run(update_ecosystem_lesson())
