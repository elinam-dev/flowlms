import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE = "http://localhost:8000/uploads/images"

courses = [
    ("pumps and pump spares",       f"{BASE}/presentation_on_pump_spares_01.png"),
    ("pump curves",                 f"{BASE}/pump_curves_01.png"),
    ("pump types",                  f"{BASE}/pump_tyres_01.png"),
    ("valves",                      f"{BASE}/valve_01.png"),
]

async def main():
    for search_term, thumbnail in courses:
        course = await db.courses.find_one({"title": {"$regex": search_term, "$options": "i"}})
        if course:
            await db.courses.update_one({"_id": course["_id"]}, {"$set": {"thumbnail": thumbnail}})
            print(f"OK: {course['title']}")
        else:
            print(f"FAIL: {search_term}")

asyncio.run(main())
