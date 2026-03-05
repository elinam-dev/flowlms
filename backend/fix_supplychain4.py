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

async def fix_supplychain4():
    lessons = await db.lessons.find({
        "content": {"$regex": "supplychain4"}
    }).to_list(None)
    
    for lesson in lessons:
        print(f"Found: {lesson['title']}")
        print(f"Current content:\n{lesson['content']}\n")
        
        # Fix the path
        new_content = lesson['content'].replace(
            'C:\\Users\\User\\Desktop\\flowlms\\flowlms\\backend\\uploads\\images\\diploma-supply-chain\\supplychain4.jpg',
            '/uploads/images/diploma-supply-chain/supplychain4.jpg'
        )
        
        if new_content != lesson['content']:
            await db.lessons.update_one(
                {"id": lesson["id"]},
                {"$set": {"content": new_content}}
            )
            print(f"Fixed! New content:\n{new_content}")
        else:
            print("Already correct")

if __name__ == "__main__":
    asyncio.run(fix_supplychain4())
