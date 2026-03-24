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

async def fix_incoterms():
    result = await db.lessons.update_many(
        {"content": {"$regex": "incoterms"}},
        [{"$set": {"content": {"$replaceAll": {"input": "$content", "find": "http://localhost:8000/uploads/images/supply_chain/incoterms/incoterms", "replacement": "http://localhost:8000/uploads/images/supply_chain/incoterms/incoterms"}}}}]
    )
    
    # Check current format
    lesson = await db.lessons.find_one({"content": {"$regex": "incoterms"}})
    if lesson:
        print(f"Current format:\n{lesson['content'][:300]}")
    
    print(f"\nShould be: http://localhost:8000/uploads/images/supply_chain/incoterms/incoterms1.jpeg")

if __name__ == "__main__":
    asyncio.run(fix_incoterms())
