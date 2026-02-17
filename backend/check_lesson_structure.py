import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def delete_and_recreate():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Delete incomplete course
    course = await db.courses.find_one({"code": "ENG-PUMP-002"})
    if course:
        course_id = str(course["_id"])
        await db.courses.delete_one({"_id": course["_id"]})
        await db.modules.delete_many({"course_id": course_id})
        await db.quizzes.delete_many({"course_id": course_id})
        print("Deleted incomplete course")
    
    # Get a sample lesson to see structure
    sample = await db.lessons.find_one()
    print(f"Sample lesson structure: {sample}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(delete_and_recreate())
