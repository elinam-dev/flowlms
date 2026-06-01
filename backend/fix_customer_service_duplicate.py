import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"

async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["flowitec_lms"]

    result = await db.courses.delete_one({"title": "Customer service skills"})
    print("Deleted lowercase duplicate:", result.deleted_count)

    remaining = await db.courses.find_one(
        {"title": {"$regex": "customer service skills", "$options": "i"}},
        {"_id": 0, "id": 1, "title": 1, "category": 1, "is_published": 1}
    )
    print("Remaining:", remaining)
    client.close()

asyncio.run(main())
