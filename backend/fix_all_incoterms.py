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

async def fix():
    # Find all lessons with incoterms in title or content
    lessons = await db.lessons.find({
        "$or": [
            {"title": {"$regex": "incoterm", "$options": "i"}},
            {"content": {"$regex": "incoterms\\d+\\.jpeg"}}
        ]
    }).to_list(200)
    
    print(f"Found {len(lessons)} incoterms lessons")
    
    # Get the correct module
    module = await db.modules.find_one({"id": "incoterms_2024_module_1"})
    
    # Update all
    for lesson in lessons:
        await db.lessons.update_one(
            {"id": lesson['id']},
            {"$set": {"module_id": module['id']}}
        )
    
    print(f"Updated {len(lessons)} lessons to module: {module['title']}")

if __name__ == "__main__":
    asyncio.run(fix())
