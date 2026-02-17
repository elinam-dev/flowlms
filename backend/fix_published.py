import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Update the Pump Curves course to be published
    result = await db.courses.update_one(
        {"code": "ENG-PUMP-002"},
        {"$set": {"is_published": True}}
    )
    
    print(f"Updated: {result.modified_count} course")
    
    # Check all courses
    courses = await db.courses.find({}, {"_id": 0, "title": 1, "code": 1, "is_published": 1}).to_list(100)
    print("\nAll courses:")
    for c in courses:
        print(f"- {c.get('title')} ({c.get('code')}) - Published: {c.get('is_published')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
