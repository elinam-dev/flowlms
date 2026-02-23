import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def clear():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    
    # Clear all progress for this course
    result = await db.progress.delete_many({"course_id": course["id"]})
    
    print(f"Cleared {result.deleted_count} progress records")
    client.close()

if __name__ == "__main__":
    asyncio.run(clear())
