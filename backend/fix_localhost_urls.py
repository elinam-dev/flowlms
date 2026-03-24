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

BACKEND_URL = "https://flowlms-production.up.railway.app"

async def fix_localhost():
    result = await db.lessons.update_many(
        {"content": {"$regex": "localhost"}},
        [{"$set": {"content": {"$replaceAll": {"input": "$content", "find": "http://localhost:8001", "replacement": BACKEND_URL}}}}]
    )
    print(f"Updated {result.modified_count} lessons (localhost:8001)")
    
    result2 = await db.lessons.update_many(
        {"content": {"$regex": "localhost"}},
        [{"$set": {"content": {"$replaceAll": {"input": "$content", "find": "http://localhost:8000", "replacement": BACKEND_URL}}}}]
    )
    print(f"Updated {result2.modified_count} lessons (localhost:8000)")

if __name__ == "__main__":
    asyncio.run(fix_localhost())
