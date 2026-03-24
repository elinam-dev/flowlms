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
    course = await db.courses.find_one({"id": "4f137bf0-9670-47a3-abdb-670bb02745ac"})
    if course:
        print(f"Course Title: {course['title']}")
        print(f"Category: {course.get('category', 'N/A')}")
        print(f"Published: {course.get('is_published', False)}")

if __name__ == "__main__":
    asyncio.run(check())
