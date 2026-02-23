import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    print(f"is_published: {course.get('is_published')}")
    
    # Publish it
    await db.courses.update_one(
        {"id": course["id"]},
        {"$set": {"is_published": True}}
    )
    
    print("Course published")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
