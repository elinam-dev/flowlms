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

async def find():
    # Search for the course with different variations
    search_terms = [
        "diploma in introduction to human resource",
        "human resource systems",
        "introduction to modern human resource",
        "top 25 excel",
        "core excel skills",
        "basics of value",
        "essentials of sap",
        "fundamentals of budgeting",
        "accounts payable",
        "accounts receive",
        "diploma in decision making",
        "cost and management accounting",
        "tax accounting systems",
        "tax accounting",
        "essentials.*throughout.*accounting",
        "throughout.*accounting",
        "lean accounting",
        "essentials.*lean.*accounting"
    ]
    
    for term in search_terms:
        course = await db.courses.find_one({"title": {"$regex": term, "$options": "i"}})
        if course:
            print(f"Found: {course['title']}")
            print(f"Course ID: {course['id']}")
            print(f"Category: {course.get('category', 'N/A')}")
            print(f"Published: {course.get('is_published', False)}")
            
            # Check modules
            modules = await db.modules.find({"course_id": course['id']}).to_list(10)
            print(f"\nModules: {len(modules)}")
            
            for module in modules:
                lessons = await db.lessons.count_documents({"module_id": module['id']})
                print(f"  - {module['title']}: {lessons} lessons")
            return
    
    print("Course not found. Let me search for similar titles...")
    
    # Search for any course with "accounting" in title
    courses = await db.courses.find({"title": {"$regex": "accounting", "$options": "i"}}).to_list(20)
    print(f"\nFound {len(courses)} courses with 'accounting':")
    for course in courses:
        print(f"  - {course['title']}")

if __name__ == "__main__":
    asyncio.run(find())