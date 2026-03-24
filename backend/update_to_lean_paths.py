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

async def update():
    result = await db.lessons.update_many(
        {"content": {"$regex": "learn_sigma_six"}},
        [{"$set": {"content": {"$replaceAll": {"input": "$content", "find": "learn_sigma_six", "replacement": "lean_sigma_six"}}}}]
    )
    print(f"Updated {result.modified_count} lessons")
    
    # Update thumbnail
    await db.courses.update_one(
        {"id": "bba65ff6-f69b-4b73-9c5d-64c822b9218f"},
        {"$set": {"thumbnail": "http://localhost:8000/uploads/images/supply_chain/lean_sigma_six.jpg"}}
    )
    print("Updated thumbnail")

if __name__ == "__main__":
    asyncio.run(update())
