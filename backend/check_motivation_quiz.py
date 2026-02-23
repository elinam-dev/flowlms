import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def check():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    print(f"Course ID: {course['id']}")
    
    quizzes = await db.quizzes.find({"course_id": course["id"]}).to_list(100)
    print(f"Quizzes found: {len(quizzes)}")
    
    for quiz in quizzes:
        print(f"  Quiz: {quiz.get('title')}")
        print(f"  Questions: {len(quiz.get('questions', []))}")
        print(f"  Module ID: {quiz.get('module_id', 'None')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check())
