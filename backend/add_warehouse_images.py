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

async def add_warehouse_images():
    course = await db.courses.find_one({
        "title": {"$regex": "warehouse.*management", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    # Get all image files from the folder
    images_dir = ROOT_DIR / "uploads" / "images" / "warehouse_management"
    image_files = sorted([f.name for f in images_dir.glob("*.jpeg")])
    
    # Update first lesson with first image
    lesson1 = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Introduction"
    })
    
    if lesson1:
        content = f'<div style="text-align: center; padding: 20px;"><img src="/uploads/images/warehouse_management/{image_files[0]}" alt="Introduction" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        await db.lessons.update_one(
            {"id": lesson1["id"]},
            {"$set": {"content": content, "content_type": "text"}}
        )
        print(f"Updated: Introduction with {image_files[0]}")
    
    # Add remaining images
    for i, img_file in enumerate(image_files[1:], start=2):
        content = f'<div style="text-align: center; padding: 20px;"><img src="/uploads/images/warehouse_management/{img_file}" alt="Warehouse Management - Part {i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": f"Warehouse Management - Part {i}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 5,
            "order": i - 1
        }
        
        await db.lessons.insert_one(lesson_doc)
        if i % 10 == 0:
            print(f"Added {i-1} lessons...")
    
    print(f"\nDone! Added {len(image_files)} image lessons")

if __name__ == "__main__":
    asyncio.run(add_warehouse_images())
