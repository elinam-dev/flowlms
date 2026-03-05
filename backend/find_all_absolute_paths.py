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

async def find_absolute_paths():
    lessons = await db.lessons.find({
        "content": {"$regex": "C:"}
    }).to_list(None)
    
    if not lessons:
        print("No absolute paths found!")
    else:
        for lesson in lessons:
            print(f"\nLesson: {lesson['title']}")
            print(f"Content: {lesson['content'][:300]}")
            
            # Fix it
            new_content = lesson['content'].replace(
                'C:\\Users\\User\\Desktop\\flowlms\\flowlms\\backend\\uploads\\images\\',
                '/uploads/images/'
            ).replace('\\', '/')
            
            await db.lessons.update_one(
                {"id": lesson["id"]},
                {"$set": {"content": new_content}}
            )
            print("FIXED!")

if __name__ == "__main__":
    asyncio.run(find_absolute_paths())
