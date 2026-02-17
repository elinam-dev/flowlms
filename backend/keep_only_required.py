import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def keep_only_required():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Delete all courses that are NOT compulsory
    courses = await db.courses.find({"course_type": {"$ne": "compulsory"}}).to_list(None)
    
    for course in courses:
        course_id = course['id']
        
        # Delete modules and lessons
        modules = await db.modules.find({"course_id": course_id}).to_list(None)
        for module in modules:
            await db.lessons.delete_many({"module_id": module['id']})
            await db.quizzes.delete_many({"module_id": module['id']})
        
        await db.modules.delete_many({"course_id": course_id})
        await db.courses.delete_one({"id": course_id})
        await db.progress.delete_many({"course_id": course_id})
        
        print(f"Deleted: {course['title']}")
    
    # Show remaining courses
    remaining = await db.courses.find({}).to_list(None)
    print(f"\nRemaining courses: {len(remaining)}")
    for c in remaining:
        print(f"  - {c['title']} ({c.get('code', 'N/A')})")
    
    client.close()

asyncio.run(keep_only_required())
