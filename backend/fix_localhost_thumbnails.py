import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def update():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    await db.courses.update_one(
        {"title": {"$regex": "Effective B2B communication", "$options": "i"}},
        {"$set": {"thumbnail": "http://127.0.0.1:8001/api/uploads/images/B2B.jpg"}}
    )
    
    await db.courses.update_one(
        {"title": {"$regex": "French", "$options": "i"}},
        {"$set": {"thumbnail": "http://127.0.0.1:8001/api/uploads/images/french.jpg"}}
    )
    
    print("Updated thumbnails to localhost URLs")
    client.close()

if __name__ == "__main__":
    asyncio.run(update())
