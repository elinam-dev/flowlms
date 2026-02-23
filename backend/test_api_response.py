import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def check():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    course_id = course["id"]
    
    # Simulate what the API does
    modules = await db.modules.find({"course_id": course_id}, {"_id": 0}).sort("order", 1).to_list(100)
    for module in modules:
        lessons = await db.lessons.find({"module_id": module["id"]}, {"_id": 0}).sort("order", 1).to_list(100)
        module["lessons"] = lessons
        
        # Get quizzes for this module
        quizzes = await db.quizzes.find({"module_id": module["id"]}, {"_id": 0}).to_list(10)
        module["quizzes"] = quizzes
        
        print(f"Module: {module['title']}")
        print(f"  Lessons: {len(lessons)}")
        print(f"  Quizzes: {len(quizzes)}")
        if quizzes:
            print(f"    Quiz title: {quizzes[0]['title']}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check())
