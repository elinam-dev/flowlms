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

async def check():
    lesson = await db.lessons.find_one({"content": {"$regex": "lean_sigma_six1"}})
    if lesson:
        print(f"Lesson: {lesson['title']}")
        print(f"Content: {lesson['content'][:200]}")
    else:
        print("No lesson found")

if __name__ == "__main__":
    asyncio.run(check())
