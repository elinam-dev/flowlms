import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

async def main():
    # Find lessons that reference image files
    lesson = await db.lessons.find_one(
        {'content': {'$regex': '/images/', '$options': 'i'}},
        {'_id': 0}
    )
    print(lesson)

asyncio.run(main())
