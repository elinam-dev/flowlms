import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def check():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    quiz = await db.quizzes.find_one({"course_id": course["id"]})
    
    print(f"Quiz: {quiz['title']}")
    print(f"\nFirst question:")
    q = quiz['questions'][0]
    print(f"  Question: {q['question']}")
    print(f"  Type: {q['type']}")
    print(f"  Correct answer: {q['correct_answer']}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check())
