import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def remove_policy_safety_ethics_quizzes():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Keywords to identify policy, safety, and ethics courses
    keywords = [
        'policy', 'policies', 'safety', 'ethics', 'conduct', 
        'disciplinary', 'code', 'health', 'employee handbook'
    ]
    
    # Get all courses
    courses = await db.courses.find({}).to_list(None)
    
    removed_count = 0
    removed_courses = []
    
    for course in courses:
        title = course['title'].lower()
        
        # Check if course title contains any of the keywords
        if any(keyword in title for keyword in keywords):
            # Find the module for this course
            module = await db.modules.find_one({"course_id": course['id']})
            if module:
                # Find and delete the quiz
                quiz = await db.quizzes.find_one({"module_id": module['id']})
                if quiz:
                    await db.quizzes.delete_one({"id": quiz['id']})
                    removed_count += 1
                    removed_courses.append(course['title'])
                    print(f"Removed quiz from: {course['title']}")
    
    print(f"\n{'='*60}")
    print(f"Total quizzes removed: {removed_count}")
    print(f"{'='*60}")
    
    if removed_courses:
        print("\nCourses with quizzes removed:")
        for title in removed_courses:
            print(f"  - {title}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(remove_policy_safety_ethics_quizzes())
