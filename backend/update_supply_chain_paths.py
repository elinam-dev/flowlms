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

async def update_paths():
    folders = [
        "incoterms",
        "diploma-supply-chain",
        "understanding_supply_risk_management",
        "B2B-supply-chain-management",
        "understanding_supply_chain_ecosystem_fundamentals_of_using_six_sigma_in_supply_chain",
        "international_marketing__and_supply_chain_management",
        "freight",
        "sea_export",
        "warehouse_management",
        "learn_sigma_six"
    ]
    
    for folder in folders:
        old_path = f"/uploads/images/{folder}/"
        new_path = f"/uploads/images/supply_chain/{folder}/"
        
        result = await db.lessons.update_many(
            {"content": {"$regex": old_path}},
            [{"$set": {"content": {"$replaceAll": {"input": "$content", "find": old_path, "replacement": new_path}}}}]
        )
        print(f"Updated {result.modified_count} lessons for {folder}")
    
    print("\nAll paths updated successfully!")

if __name__ == "__main__":
    asyncio.run(update_paths())
