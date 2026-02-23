import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def check():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    courses = await db.courses.find({}, {"_id": 0, "title": 1, "code": 1, "category": 1}).to_list(100)
    print("All courses:")
    for c in courses:
        print(f"- {c.get('title')} | Code: {c.get('code')} | Category: {c.get('category')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check())
