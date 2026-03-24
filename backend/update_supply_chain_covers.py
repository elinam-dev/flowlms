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

courses = [
    {"title": "incoterm", "cover": "incoterms.jpeg"},
    {"title": "Diploma in supply chain", "cover": "diploma-supply-chain.jpg"},
    {"title": "supply chain risk", "cover": "understanding_supply_risk_management.jpg"},
    {"title": "B2B supply chain", "cover": "B2B-supply-chain-management.jpg"},
    {"title": "ecosystem", "cover": "understanding_supply_chain_ecosystem_fundamentals_of_using_six_sigma_in_supply_chain.jpg"},
    {"title": "International marketing and supply", "cover": "international_marketing__and_supply_chain_management.jpg"},
    {"title": "Freight broker", "cover": "freight.jpg"},
    {"title": "sea export", "cover": "sea_export.jpg"},
    {"title": "Warehouse management", "cover": "warehouse_management.jpg"},
    {"title": "six sigma", "cover": "learn_sigma_six.jpg"}
]

async def update():
    for item in courses:
        course = await db.courses.find_one({"title": {"$regex": item["title"], "$options": "i"}})
        if course:
            await db.courses.update_one(
                {"id": course['id']},
                {"$set": {"thumbnail": f"http://localhost:8000/uploads/images/supply_chain/{item['cover']}"}}
            )
            print(f"Updated: {course['title']}")
        else:
            print(f"Not found: {item['title']}")

if __name__ == "__main__":
    asyncio.run(update())
