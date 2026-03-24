import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def create():
    course = await db.courses.find_one({"id": "bba65ff6-f69b-4b73-9c5d-64c822b9218f"})
    
    # Create module
    module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": module_id,
        "course_id": course['id'],
        "title": "Learn Six Sigma Fundamentals",
        "order": 0
    })
    
    # Create 70 lessons
    for i in range(1, 71):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": f"Learn Six Sigma - Slide {i}",
            "content_type": "text",
            "content": f'<div style="text-align: center;"><img src="http://localhost:8000/uploads/images/supply_chain/learn_sigma_six/learn_sigma_six{i}.jpeg" alt="Learn Six Sigma Slide {i}" style="max-width: 100%; height: auto;" /></div>',
            "duration_minutes": 5,
            "order": i - 1
        })
    
    print(f"Created 70 lessons for {course['title']}")

if __name__ == "__main__":
    asyncio.run(create())
