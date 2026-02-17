import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def delete():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"code": "ENG-PUMP-001"})
    if course:
        course_id = course["id"]
        await db.courses.delete_one({"id": course_id})
        
        modules = await db.modules.find({"course_id": course_id}).to_list(100)
        for module in modules:
            await db.lessons.delete_many({"module_id": module["id"]})
        
        await db.modules.delete_many({"course_id": course_id})
        await db.quizzes.delete_many({"course_id": course_id})
        await db.progress.delete_many({"course_id": course_id})
        
        print("Deleted Pump Spares course")
    else:
        print("Course not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(delete())
