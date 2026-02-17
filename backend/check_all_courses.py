import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def check():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    courses = await db.courses.find().to_list(length=100)
    print(f"Total courses: {len(courses)}\n")
    
    for c in courses:
        print(f"- {c.get('title')} (Code: {c.get('code')})")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check())
