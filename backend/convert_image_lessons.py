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

async def convert_image_lessons():
    """Convert image-type lessons to have HTML img tags"""
    
    lessons = await db.lessons.find({"content_type": "image"}).to_list(None)
    
    updated = 0
    for lesson in lessons:
        content = lesson.get("content", "")
        
        # If content is just a URL, wrap it in an img tag
        if content.startswith("/uploads/") or content.startswith("http"):
            new_content = f'<div style="text-align: center; padding: 20px;"><img src="{content}" alt="{lesson["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
            
            await db.lessons.update_one(
                {"id": lesson["id"]},
                {"$set": {
                    "content": new_content,
                    "content_type": "text"  # Change to text so it renders as HTML
                }}
            )
            print(f"Converted: {lesson['title']}")
            updated += 1
    
    print(f"\nTotal converted: {updated} lessons")

if __name__ == "__main__":
    asyncio.run(convert_image_lessons())
