import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def delete_image_courses():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    codes = ["ENG-PUMP-001", "ENG-PUMP-002", "ENG-PUMP-003", "ENG-VALVE-001"]
    
    for code in codes:
        course = await db.courses.find_one({"code": code})
        if course:
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
    
    print("\nAll image courses deleted!")
    client.close()

asyncio.run(delete_image_courses())
