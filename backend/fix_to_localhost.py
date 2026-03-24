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

async def fix_to_localhost():
    result = await db.lessons.update_many(
        {"content": {"$regex": "flowlms-production.up.railway.app"}},
        [{"$set": {"content": {"$replaceAll": {"input": "$content", "find": "https://flowlms-production.up.railway.app", "replacement": "http://localhost:8001"}}}}]
    )
    print(f"Updated {result.modified_count} lessons to localhost")

if __name__ == "__main__":
    asyncio.run(fix_to_localhost())
