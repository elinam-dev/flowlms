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
    result = await db.courses.update_one(
        {"title": {"$regex": "ecosystem.*six sigma", "$options": "i"}},
        {"$set": {"thumbnail": "http://localhost:8000/uploads/images/supply_chain/understanding_supply_risk_management.jpg"}}
    )
    print(f"Updated {result.modified_count} course")

if __name__ == "__main__":
    asyncio.run(update())
