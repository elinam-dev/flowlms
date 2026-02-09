import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def clean_courses():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Delete all existing courses, modules, lessons, and progress
    await db.courses.delete_many({})
    await db.modules.delete_many({})
    await db.lessons.delete_many({})
    await db.progress.delete_many({})
    await db.quizzes.delete_many({})
    
    # Reset enrolled_courses for all users
    await db.users.update_many({}, {"$set": {"enrolled_courses": [], "completed_courses": []}})
    
    print("All courses cleaned. Restart the backend to seed new courses.")
    client.close()

if __name__ == "__main__":
    asyncio.run(clean_courses())
