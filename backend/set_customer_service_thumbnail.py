import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"

async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["flowitec_lms"]

    result = await db.courses.update_one(
        {"id": "customer_service_skills_2024"},
        {"$set": {"thumbnail": "https://flowlms-production.up.railway.app/uploads/images/petr-machacek-BeVGrXEktIk-unsplash.jpg"}}
    )
    print("Updated:", result.modified_count)
    course = await db.courses.find_one({"id": "customer_service_skills_2024"}, {"_id": 0, "title": 1, "thumbnail": 1})
    print(course)
    client.close()

asyncio.run(main())
