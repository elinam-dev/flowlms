import asyncio, os, uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

RAILWAY = "https://flowlms-production.up.railway.app"
MODULE_ID = "incoterms_2024_module_1"

async def seed():
    lessons = []
    for i in range(1, 87):
        lessons.append({
            "id": str(uuid.uuid4()),
            "module_id": MODULE_ID,
            "title": f"Slide {i}",
            "content_type": "text",
            "content": f'<div class="slide-container"><img src="{RAILWAY}/api/uploads/images/supply_chain/incoterms/incoterms{i}.jpeg" alt="Incoterms Slide {i}" style="width:100%;max-width:900px;height:auto;display:block;margin:0 auto;" /></div>',
            "duration_minutes": 2,
            "order": i - 1
        })

    await db.lessons.insert_many(lessons)
    print(f"Created {len(lessons)} incoterms lessons")
    client.close()

asyncio.run(seed())
