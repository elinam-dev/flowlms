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

async def fix_image_tags():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    modules = await db.modules.find({"course_id": course["id"]}).to_list(None)
    
    for module in modules:
        lessons = await db.lessons.find({"module_id": module["id"]}).to_list(None)
        
        for lesson in lessons:
            content = lesson.get("content", "")
            
            # Check if content has img tag with src attribute
            if "<img" in content and "src=" in content:
                # Fix img tags - ensure they have proper styling
                new_content = content.replace(
                    '<img src="',
                    '<img src="'
                ).replace(
                    'style="max-width: 100%; margin-top: 20px;"',
                    'style="max-width: 100%; height: auto; display: block; margin: 20px auto;"'
                ).replace(
                    'style="max-width: 100%; margin: 20px 0;"',
                    'style="max-width: 100%; height: auto; display: block; margin: 20px auto;"'
                ).replace(
                    'style="max-width: 100%; margin-top: 10px;"',
                    'style="max-width: 100%; height: auto; display: block; margin: 10px auto;"'
                )
                
                if new_content != content:
                    await db.lessons.update_one(
                        {"id": lesson["id"]},
                        {"$set": {"content": new_content}}
                    )
                    print(f"Fixed image tag in: {lesson['title']}")
            
            # Show current content for debugging
            if "/uploads/images/" in content:
                print(f"\n{lesson['title']}:")
                print(f"  Type: {lesson.get('content_type')}")
                print(f"  Content preview: {content[:200]}...")

if __name__ == "__main__":
    asyncio.run(fix_image_tags())
