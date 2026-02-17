import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def check_courses():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    courses = await db.courses.find({}).to_list(None)
    print(f"Total courses: {len(courses)}\n")
    for c in courses:
        print(f"- {c['title']} ({c.get('code', 'N/A')}) - {c.get('course_type', 'N/A')}")
    
    client.close()

asyncio.run(check_courses())
