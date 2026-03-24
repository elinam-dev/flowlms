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
    result = await db.courses.update_one(
        {"id": "5dcf3289-dd1f-44cc-98ea-aa1345c89dde"},
        {"$set": {"title": "Essentials of throughput accounting and lean accounting"}}
    )
    print(f"Updated {result.modified_count} course")

if __name__ == "__main__":
    asyncio.run(fix())