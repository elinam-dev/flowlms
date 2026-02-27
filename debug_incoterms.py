import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

async def debug_incoterms():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Find Incoterms course
    incoterms_course = await db.courses.find_one({"title": {"$regex": "incoterms", "$options": "i"}})
    
    if not incoterms_course:
        print("No Incoterms course found")
        return
    
    print(f"Found course: {incoterms_course['title']}")
    print(f"Course ID: {incoterms_course['id']}")
    print(f"Published: {incoterms_course.get('is_published', False)}")
    
    # Get modules
    modules = await db.modules.find({"course_id": incoterms_course["id"]}).to_list(100)
    print(f"Modules found: {len(modules)}")
    
    for module in modules:
        print(f"  Module: {module['title']} (ID: {module['id']})")
        
        # Get lessons for this module
        lessons = await db.lessons.find({"module_id": module["id"]}).sort("order", 1).to_list(100)
        print(f"    Lessons: {len(lessons)}")
        
        for lesson in lessons:
            print(f"      - {lesson['title']} (Order: {lesson.get('order', 0)})")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_incoterms())