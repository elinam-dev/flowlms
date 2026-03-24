import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import re

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

BACKEND_URL = "https://flowlms-production.up.railway.app"

async def fix_paths():
    patterns = [
        (r'/uploads/images/incoterms(\d+)\.jpeg', f'{BACKEND_URL}/uploads/images/supply_chain/incoterms/incoterms\\1.jpeg'),
        (r'/uploads/images/supplychain(\d+)\.(jpg|jpeg)', f'{BACKEND_URL}/uploads/images/supply_chain/diploma-supply-chain/supplychain\\1.\\2'),
        (r'/uploads/images/supplyrisk(\d+)\.jpeg', f'{BACKEND_URL}/uploads/images/supply_chain/understanding_supply_risk_management/supplyrisk\\1.jpeg'),
        (r'/uploads/images/b2bsupply(\d+)\.jpeg', f'{BACKEND_URL}/uploads/images/supply_chain/B2B-supply-chain-management/b2bsupply\\1.jpeg'),
        (r'/uploads/images/ecosystem(\d+)\.jpeg', f'{BACKEND_URL}/uploads/images/supply_chain/understanding_supply_chain_ecosystem_fundamentals_of_using_six_sigma_in_supply_chain/ecosystem\\1.jpeg'),
        (r'/uploads/images/internationalmarketing(\d+)\.jpeg', f'{BACKEND_URL}/uploads/images/supply_chain/international_marketing__and_supply_chain_management/internationalmarketing\\1.jpeg'),
        (r'/uploads/images/freight(\d+)\.jpeg', f'{BACKEND_URL}/uploads/images/supply_chain/freight/freight\\1.jpeg'),
        (r'/uploads/images/sea_export(\d+)\.jpeg', f'{BACKEND_URL}/uploads/images/supply_chain/sea_export/sea_export\\1.jpeg'),
        (r'/uploads/images/warehouse_management(\d+)\.jpeg', f'{BACKEND_URL}/uploads/images/supply_chain/warehouse_management/warehouse_management\\1.jpeg'),
        (r'/uploads/images/learn_sigma_six(\d+)\.jpeg', f'{BACKEND_URL}/uploads/images/supply_chain/learn_sigma_six/learn_sigma_six\\1.jpeg'),
    ]
    
    total_updated = 0
    for pattern, replacement in patterns:
        lessons = await db.lessons.find({"content": {"$regex": pattern}}).to_list(1000)
        
        for lesson in lessons:
            new_content = re.sub(pattern, replacement, lesson['content'])
            await db.lessons.update_one(
                {"id": lesson["id"]},
                {"$set": {"content": new_content}}
            )
            total_updated += 1
        
        print(f"Updated {len(lessons)} lessons for pattern: {pattern}")
    
    print(f"\nTotal lessons updated: {total_updated}")

if __name__ == "__main__":
    asyncio.run(fix_paths())
