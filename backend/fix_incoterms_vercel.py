"""
Fix corrupted incoterms image URLs.
Broken: https://flowlms-production.up.railway.app/apihttps://flowlms-production.up.railway.app/uploads/images/supply_chain/incoterms/incotermsX.jpeg
Fixed:  https://flowlms-production.up.railway.app/api/uploads/images/supply_chain/incoterms/incotermsX.jpeg
"""
import asyncio, os, re
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

RAILWAY = "https://flowlms-production.up.railway.app"
BROKEN  = f"{RAILWAY}/apihttps://flowlms-production.up.railway.app/uploads/"
FIXED   = f"{RAILWAY}/api/uploads/"

async def fix():
    lessons = await db.lessons.find({"content": {"$regex": "apihttps://"}}).to_list(None)
    print(f"Found {len(lessons)} broken lessons")

    for lesson in lessons:
        new_content = lesson["content"].replace(BROKEN, FIXED)
        await db.lessons.update_one({"id": lesson["id"]}, {"$set": {"content": new_content}})
        print(f"  Fixed: {lesson['title']}")

    print(f"\nDone. Fixed {len(lessons)} lessons.")
    client.close()

asyncio.run(fix())
