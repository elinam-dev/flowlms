import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

async def main():
    # Check a sample learner
    user = await db.users.find_one({'role': 'learner'}, {'_id': 0, 'id': 1, 'email': 1, 'enrolled_courses': 1})
    print("Sample user:", user)

    # Check total users
    total = await db.users.count_documents({'role': 'learner'})
    print(f"Total learners: {total}")

    # Check a sample course enrolled_users
    course = await db.courses.find_one({}, {'_id': 0, 'id': 1, 'title': 1, 'enrolled_users': 1})
    print("Sample course:", course)

    # Check progress collection
    prog = await db.progress.find_one({}, {'_id': 0})
    print("Sample progress:", prog)

asyncio.run(main())
