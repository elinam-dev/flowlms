import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

async def main():
    courses = await db.courses.find(
        {"category": {"$regex": "hr|human resource", "$options": "i"}},
        {"_id": 0, "id": 1, "title": 1, "category": 1, "course_type": 1, "published": 1}
    ).to_list(200)
    print(f"Found {len(courses)} HR courses:\n")
    for c in courses:
        print(f"  - [{c.get('course_type','?')}] {c['title']} | category: {c.get('category')} | published: {c.get('published')}")

asyncio.run(main())
