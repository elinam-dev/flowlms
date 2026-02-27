import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def verify_published():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Count all courses
    total = await db.courses.count_documents({})
    print(f"Total courses in DB: {total}")
    
    # Count published courses
    published = await db.courses.count_documents({"is_published": True})
    print(f"Published courses: {published}")
    
    # Count unpublished
    unpublished = await db.courses.count_documents({"is_published": {"$ne": True}})
    print(f"Unpublished courses: {unpublished}")
    
    # Get published courses (what the API returns)
    courses = await db.courses.find({"is_published": True}, {"_id": 0, "title": 1}).to_list(100)
    print(f"\nPublished courses that will show in frontend:")
    for i, c in enumerate(courses, 1):
        print(f"{i}. {c.get('title')}")
    
    client.close()

if __name__ == '__main__':
    asyncio.run(verify_published())
