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

async def add_inline_images():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    # 1. Add image at end of Module 3.1 (EOQ)
    module3 = await db.modules.find_one({
        "course_id": course["id"],
        "title": {"$regex": "Module 3.*Inventory"}
    })
    
    lesson_3_1 = await db.lessons.find_one({
        "module_id": module3["id"],
        "title": {"$regex": "3.1.*EOQ"}
    })
    
    if lesson_3_1:
        new_content = lesson_3_1["content"] + '\n<img src="C:\\Users\\User\\Desktop\\flowlms\\flowlms\\backend\\uploads\\images\\diploma in supply chain\\supplychain4.jpg" alt="EOQ Formula" style="max-width: 100%; margin-top: 20px;">'
        await db.lessons.update_one({"id": lesson_3_1["id"]}, {"$set": {"content": new_content}})
        print("Added image to Module 3.1 (EOQ)")
    
    # 2. Add image after Module 5 (as new lesson)
    module5 = await db.modules.find_one({
        "course_id": course["id"],
        "title": {"$regex": "Module 5.*Digital"}
    })
    
    if module5:
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module5["id"],
            "title": "Digital Transformation Visual",
            "content_type": "image",
            "content": r"C:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\diploma in supply chain\supplychain5.jpg",
            "duration_minutes": 5,
            "order": 2
        }
        await db.lessons.insert_one(lesson_doc)
        print("Added image after Module 5")
    
    # 3. Add image after "The Formula:" in Module 6.1 (C2C)
    module6 = await db.modules.find_one({
        "course_id": course["id"],
        "title": {"$regex": "Module 6.*Finance"}
    })
    
    lesson_6_1 = await db.lessons.find_one({
        "module_id": module6["id"],
        "title": {"$regex": "6.1.*C2C"}
    })
    
    if lesson_6_1:
        content = lesson_6_1["content"]
        # Insert image after "The Formula:"
        new_content = content.replace(
            '<h4>The Formula:</h4>',
            '<h4>The Formula:</h4>\n<img src="C:\\Users\\User\\Desktop\\flowlms\\flowlms\\backend\\uploads\\images\\diploma in supply chain\\supplychain6.jpg" alt="C2C Formula" style="max-width: 100%; margin: 20px 0;">'
        )
        await db.lessons.update_one({"id": lesson_6_1["id"]}, {"$set": {"content": new_content}})
        print("Added image to Module 6.1 (C2C Formula)")
    
    # 4. Add image after "Exponential Smoothing" in Module 9.1
    module9 = await db.modules.find_one({
        "course_id": course["id"],
        "title": {"$regex": "Module 9.*Forecasting"}
    })
    
    lesson_9_1 = await db.lessons.find_one({
        "module_id": module9["id"],
        "title": {"$regex": "9.1.*Quantitative"}
    })
    
    if lesson_9_1:
        content = lesson_9_1["content"]
        # Insert image after Exponential Smoothing
        new_content = content.replace(
            '<li><strong>Exponential Smoothing:</strong> Weighting recent data more heavily (where α is the smoothing constant, A is actual demand, and F is the forecast).</li>',
            '<li><strong>Exponential Smoothing:</strong> Weighting recent data more heavily (where α is the smoothing constant, A is actual demand, and F is the forecast).<br><img src="C:\\Users\\User\\Desktop\\flowlms\\flowlms\\backend\\uploads\\images\\diploma in supply chain\\supplychain7.jpg" alt="Exponential Smoothing Formula" style="max-width: 100%; margin-top: 10px;"></li>'
        )
        await db.lessons.update_one({"id": lesson_9_1["id"]}, {"$set": {"content": new_content}})
        print("Added image to Module 9.1 (Exponential Smoothing)")

if __name__ == "__main__":
    asyncio.run(add_inline_images())
