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

async def update_first_lesson():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    if not course:
        print("Course not found!")
        return
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    if not module:
        print("Module not found!")
        return
    
    # Get first lesson (Introduction)
    lesson = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Introduction"
    })
    
    if not lesson:
        print("Introduction lesson not found!")
        return
    
    # Update with image
    image_path = r"C:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\diploma in supply chain\supplychain1.jpeg"
    
    await db.lessons.update_one(
        {"id": lesson["id"]},
        {"$set": {
            "content_type": "image",
            "content": image_path
        }}
    )
    
    print(f"Updated lesson: {lesson['title']}")
    print(f"Content type: image")
    print(f"Image path: {image_path}")

if __name__ == "__main__":
    asyncio.run(update_first_lesson())
