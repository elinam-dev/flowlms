import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

async def main():
    course = await db.courses.find_one(
        {'title': {'$regex': 'HR Analytics', '$options': 'i'}},
        {'_id': 0, 'id': 1, 'title': 1, 'published': 1, 'is_published': 1, 'category': 1}
    )
    print("Before:", course)

    await db.courses.update_one(
        {'id': course['id']},
        {'$set': {'published': True, 'is_published': True}}
    )
    print("Published successfully.")

asyncio.run(main())
