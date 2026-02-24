import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def update():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    await db.courses.update_one(
        {"title": {"$regex": "french", "$options": "i"}},
        {"$set": {"thumbnail": "http://127.0.0.1:8000/api/uploads/images/french.jpg"}}
    )
    
    print("Updated French course thumbnail")
    client.close()

if __name__ == "__main__":
    asyncio.run(update())
