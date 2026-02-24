import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def find():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": {"$regex": "french", "$options": "i"}})
    
    if course:
        print(f"Found course:")
        print(f"  Title: {course['title']}")
        print(f"  Category: {course.get('category')}")
        print(f"  ID: {course['id']}")
        print(f"  Published: {course.get('is_published')}")
        
        modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
        print(f"  Modules: {len(modules)}")
        
        for module in modules:
            lessons = await db.lessons.find({"module_id": module["id"]}).to_list(100)
            print(f"    Module: {module['title']} - {len(lessons)} lessons")
    else:
        print("French course not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(find())
