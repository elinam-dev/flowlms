import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def check():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    print(f"Course: {course['title']}")
    print(f"Course ID: {course['id']}")
    
    modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
    print(f"\nModules: {len(modules)}")
    
    for module in modules:
        print(f"  Module: {module['title']}")
        lessons = await db.lessons.find({"module_id": module["id"]}).to_list(100)
        print(f"  Lessons: {len(lessons)}")
        for lesson in lessons:
            print(f"    - {lesson['title']}")
            print(f"      Content preview: {lesson['content'][:100]}...")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check())
