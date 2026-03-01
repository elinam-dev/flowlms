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

async def update_embed():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"], "title": "Course Content"})
    
    lesson = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Supply Chain Networks"
    })
    
    if not lesson:
        print("Lesson not found!")
        return
    
    # Update with bigger frame and centered
    new_content = '<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/95265089?quality=720p" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
    
    await db.lessons.update_one(
        {"id": lesson["id"]},
        {"$set": {"content": new_content}}
    )
    
    print(f"Updated: {lesson['title']}")
    print("Frame size: 960x540 (centered)")

if __name__ == "__main__":
    asyncio.run(update_embed())
