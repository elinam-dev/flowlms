import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    await db.courses.update_one(
        {"title": "Motivation - Power Guide to motivating yourself and others"},
        {"$set": {"thumbnail": "http://127.0.0.1:8000/api/uploads/images/motivation.jpg"}}
    )
    
    print("Updated thumbnail to localhost")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
