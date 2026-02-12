"""
Debug quiz structure and find missing quizzes
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def debug_quizzes():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Check total counts
    total_courses = await db.courses.count_documents({})
    total_modules = await db.modules.count_documents({})
    total_quizzes = await db.quizzes.count_documents({})
    
    print(f"Database Overview:")
    print(f"  Courses: {total_courses}")
    print(f"  Modules: {total_modules}")
    print(f"  Quizzes: {total_quizzes}")
    print(f"\n{'='*80}\n")
    
    # Sample one quiz to see structure
    sample_quiz = await db.quizzes.find_one({})
    if sample_quiz:
        print("Sample Quiz Structure:")
        print(f"  Keys: {list(sample_quiz.keys())}")
        print(f"  Module ID field: {sample_quiz.get('module_id', 'NOT FOUND')}")
    
    print(f"\n{'='*80}\n")
    
    # Check each course
    courses = await db.courses.find({}).sort("title", 1).to_list(None)
    missing = []
    
    for course in courses:
        title = course['title']
        course_id = course['id']
        
        # Find module
        module = await db.modules.find_one({"course_id": course_id})
        
        if not module:
            print(f"MISSING MODULE {title}")
            missing.append(title)
            continue
        
        module_id = module['id']
        
        # Find quiz - try different field names
        quiz1 = await db.quizzes.find_one({"module_id": module_id})
        quiz2 = await db.quizzes.find_one({"moduleId": module_id})
        quiz3 = await db.quizzes.find_one({"course_id": course_id})
        
        if quiz1 or quiz2 or quiz3:
            print(f"OK {title}")
        else:
            print(f"MISSING {title} - NO QUIZ (module_id: {module_id})")
            missing.append(title)
    
    print(f"\n{'='*80}")
    print(f"\nMissing Quizzes: {len(missing)}")
    for title in missing:
        print(f"  - {title}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_quizzes())
