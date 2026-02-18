import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Update all lessons with localhost URLs
    lessons = await db.lessons.find({"content": {"$regex": "127.0.0.1:8000"}}).to_list(1000)
    
    for lesson in lessons:
        new_content = lesson["content"].replace(
            "http://127.0.0.1:8000",
            "https://flowlms-production.up.railway.app"
        )
        await db.lessons.update_one(
            {"_id": lesson["_id"]},
            {"$set": {"content": new_content}}
        )
    
    print(f"Updated {len(lessons)} lessons")
    
    # Update course thumbnails
    courses = await db.courses.find({"thumbnail": {"$regex": "127.0.0.1:8000"}}).to_list(100)
    
    for course in courses:
        new_thumbnail = course["thumbnail"].replace(
            "http://127.0.0.1:8000",
            "https://flowlms-production.up.railway.app"
        )
        await db.courses.update_one(
            {"_id": course["_id"]},
            {"$set": {"thumbnail": new_thumbnail}}
        )
    
    print(f"Updated {len(courses)} course thumbnails")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
