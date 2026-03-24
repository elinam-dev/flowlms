import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def check():
    course = await db.courses.find_one({"id": "bba65ff6-f69b-4b73-9c5d-64c822b9218f"})
    print(f"Course: {course['title']}")
    
    modules = await db.modules.find({"course_id": course['id']}).to_list(10)
    print(f"Modules: {len(modules)}")
    
    for module in modules:
        lessons = await db.lessons.find({"module_id": module['id']}).to_list(100)
        print(f"  Module '{module['title']}': {len(lessons)} lessons")

if __name__ == "__main__":
    asyncio.run(check())
