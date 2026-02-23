import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Update all courses with personal_branding category
    result = await db.courses.update_many(
        {"category": "personal_branding"},
        {"$set": {"category": "Personal Branding"}}
    )
    
    print(f"Updated {result.modified_count} courses")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
