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

async def fix_port():
    result = await db.lessons.update_many(
        {"content": {"$regex": "localhost:8001"}},
        [{"$set": {"content": {"$replaceAll": {"input": "$content", "find": "http://localhost:8001", "replacement": "http://localhost:8000"}}}}]
    )
    print(f"Updated {result.modified_count} lessons to port 8000")

if __name__ == "__main__":
    asyncio.run(fix_port())
