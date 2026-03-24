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

async def check_all():
    patterns = [
        'incoterms',
        'supplychain',
        'supplyrisk',
        'b2bsupply',
        'ecosystem',
        'internationalmarketing',
        'freight',
        'sea_export',
        'warehouse_management',
        'learn_sigma_six'
    ]
    
    for pattern in patterns:
        # Check for old paths (without supply_chain folder)
        old_path = await db.lessons.find_one(
            {"content": {"$regex": f"/uploads/images/{pattern}"}},
            {"_id": 0, "title": 1, "content": 1}
        )
        
        if old_path:
            print(f"\n{pattern}: NEEDS FIX")
            print(f"Sample: {old_path['content'][:200]}")
        else:
            print(f"\n{pattern}: OK")

if __name__ == "__main__":
    asyncio.run(check_all())
