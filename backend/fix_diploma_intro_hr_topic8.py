#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def fix():
    course = await db.courses.find_one(
        {'title': {'$regex': 'diploma in introduction to human resource', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_ids = [m['id'] for m in modules]

    # Find Topic 7 (order=6)
    lesson = await db.lessons.find_one({'module_id': {'$in': module_ids}, 'order': 6})
    new_content = '<div style="text-align: center;"><iframe src="https://player.vimeo.com/video/1094767297?quality=720p&audiotrack=main&texttrack=en" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
    await db.lessons.update_one({"_id": lesson["_id"]}, {"$set": {"content": new_content}})
    print(f"Fixed Topic 7 -> Vimeo 1094767297")

if __name__ == "__main__":
    asyncio.run(fix())
