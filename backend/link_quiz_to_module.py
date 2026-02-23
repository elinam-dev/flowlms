import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
    module_id = modules[0]["id"]
    
    # Update quiz to include module_id
    await db.quizzes.update_one(
        {"course_id": course["id"]},
        {"$set": {"module_id": module_id}}
    )
    
    print("Linked quiz to module")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
