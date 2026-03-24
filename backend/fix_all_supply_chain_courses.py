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

courses_map = [
    {"pattern": "supplychain", "title": "Diploma in supply chain management", "cover": "supplychain.jpeg"},
    {"pattern": "supplyrisk", "title": "Understanding supply chain risk management", "cover": "supplyrisk.jpeg"},
    {"pattern": "b2bsupply", "title": "B2B supply chain management", "cover": "b2bsupply.jpeg"},
    {"pattern": "ecosystem", "title": "Understanding supply chain ecosystem", "cover": "ecosystem.jpeg"},
    {"pattern": "internationalmarketing", "title": "International marketing and supply chain management", "cover": "internationalmarketing.jpeg"},
    {"pattern": "freight", "title": "Freight broker training", "cover": "freight.jpeg"},
    {"pattern": "sea_export", "title": "sea export", "cover": "sea_export.jpeg"},
    {"pattern": "warehouse_management", "title": "Warehouse management", "cover": "warehouse_management.jpeg"},
    {"pattern": "learn_sigma_six", "title": "six sigma", "cover": "learn_sigma_six.jpeg"}
]

async def fix_all():
    for item in courses_map:
        # Find course
        course = await db.courses.find_one({"title": {"$regex": item["title"], "$options": "i"}})
        if not course:
            print(f"Course not found: {item['title']}")
            continue
        
        print(f"\nFound: {course['title']}")
        
        # Find or create module
        module = await db.modules.find_one({"course_id": course['id']})
        if not module:
            import uuid
            module_id = str(uuid.uuid4())
            await db.modules.insert_one({
                "id": module_id,
                "course_id": course['id'],
                "title": "Course Content",
                "order": 0
            })
            module = await db.modules.find_one({"id": module_id})
            print(f"  Created module")
        
        # Update lessons
        result = await db.lessons.update_many(
            {"content": {"$regex": item["pattern"]}},
            {"$set": {"module_id": module['id']}}
        )
        print(f"  Updated {result.modified_count} lessons")
        
        # Update thumbnail
        folder = item["pattern"].replace("_", "_")
        if item["pattern"] == "ecosystem":
            folder = "understanding_supply_chain_ecosystem_fundamentals_of_using_six_sigma_in_supply_chain"
        elif item["pattern"] == "supplyrisk":
            folder = "understanding_supply_risk_management"
        elif item["pattern"] == "b2bsupply":
            folder = "B2B-supply-chain-management"
        elif item["pattern"] == "supplychain":
            folder = "diploma-supply-chain"
        elif item["pattern"] == "internationalmarketing":
            folder = "international_marketing__and_supply_chain_management"
        
        await db.courses.update_one(
            {"id": course['id']},
            {"$set": {"thumbnail": f"http://localhost:8000/uploads/images/supply_chain/{folder}/{item['cover']}"}}
        )
        print(f"  Updated thumbnail")

if __name__ == "__main__":
    asyncio.run(fix_all())
