#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import shutil

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def rename_warehouse_images():
    images_dir = ROOT_DIR / "uploads" / "images" / "warehouse_management"
    image_files = sorted([f for f in images_dir.glob("*.jpeg")])
    
    # Rename files
    renamed_map = {}
    for i, old_file in enumerate(image_files, start=1):
        new_name = f"warehouse_management{i}.jpeg"
        new_path = images_dir / new_name
        
        if old_file.name != new_name:
            shutil.move(str(old_file), str(new_path))
            renamed_map[old_file.name] = new_name
            if i % 20 == 0:
                print(f"Renamed {i} files...")
    
    print(f"\nRenamed {len(renamed_map)} files")
    
    # Update database
    course = await db.courses.find_one({
        "title": {"$regex": "warehouse.*management", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    lessons = await db.lessons.find({"module_id": module["id"]}).to_list(None)
    
    updated = 0
    for lesson in lessons:
        content = lesson.get("content", "")
        for old_name, new_name in renamed_map.items():
            if old_name in content:
                new_content = content.replace(old_name, new_name)
                await db.lessons.update_one(
                    {"id": lesson["id"]},
                    {"$set": {"content": new_content}}
                )
                updated += 1
                break
    
    print(f"Updated {updated} lessons in database")

if __name__ == "__main__":
    asyncio.run(rename_warehouse_images())
