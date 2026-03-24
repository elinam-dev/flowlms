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

async def check_lessons():
    # Get a sample lesson from incoterms
    lesson = await db.lessons.find_one(
        {"content": {"$regex": "incoterms"}},
        {"_id": 0, "title": 1, "content": 1}
    )
    
    if lesson:
        print(f"Title: {lesson['title']}\n")
        print(f"Content preview (first 500 chars):\n{lesson['content'][:500]}\n")
    else:
        print("No lesson found")

if __name__ == "__main__":
    asyncio.run(check_lessons())
