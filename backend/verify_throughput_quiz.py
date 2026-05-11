import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"

async def check():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["flowitec_lms"]
    q = await db.quizzes.find_one({"title": {"$regex": "throughput", "$options": "i"}})
    if q:
        print(f"FOUND: {q['title']} - {len(q['questions'])} questions")
    else:
        print("NOT FOUND")
    client.close()

asyncio.run(check())
