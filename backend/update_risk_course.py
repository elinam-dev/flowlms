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

async def update_risk_course():
    course = await db.courses.find_one({
        "title": {"$regex": "understanding.*supply.*chain.*risk", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    # Update first lesson with image
    lesson1 = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Introduction"
    })
    
    if lesson1:
        await db.lessons.update_one(
            {"id": lesson1["id"]},
            {"$set": {
                "content_type": "image",
                "content": "/uploads/images/understanding-supply-risk-management/supplyrisk1.jpeg"
            }}
        )
        print(f"Updated: {lesson1['title']} with image")
    
    # Add video lesson 1
    lesson2_content = '<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/104927716?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
    
    lesson2 = {
        "id": str(uuid.uuid4()),
        "module_id": module["id"],
        "title": "Supply Chain Risk - Part 1",
        "content_type": "embed",
        "content": lesson2_content,
        "duration_minutes": 10,
        "order": 1
    }
    await db.lessons.insert_one(lesson2)
    print("Added: Supply Chain Risk - Part 1")
    
    # Add video lesson 2
    lesson3_content = '<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/104928950?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
    
    lesson3 = {
        "id": str(uuid.uuid4()),
        "module_id": module["id"],
        "title": "Supply Chain Risk - Part 2",
        "content_type": "embed",
        "content": lesson3_content,
        "duration_minutes": 10,
        "order": 2
    }
    await db.lessons.insert_one(lesson3)
    print("Added: Supply Chain Risk - Part 2")
    
    print("\nDone! Course updated with 3 lessons")

if __name__ == "__main__":
    asyncio.run(update_risk_course())
