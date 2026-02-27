import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def check_courses():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Get all courses
    courses = await db.courses.find({}).to_list(None)
    print(f'Total courses in DB: {len(courses)}')
    
    # Find Incoterms course
    incoterms = [c for c in courses if 'incoterm' in c.get('title', '').lower()]
    
    if incoterms:
        print(f'\nFound {len(incoterms)} Incoterms course(s):')
        for course in incoterms:
            print(f"\nTitle: {course.get('title')}")
            print(f"ID: {course.get('id')}")
            print(f"Published: {course.get('is_published')}")
            print(f"Category: {course.get('category')}")
            print(f"Course Type: {course.get('course_type')}")
    else:
        print('\nNo Incoterms course found!')
    
    # Check if there's a limit in the API
    print(f'\n\nAll course titles:')
    for i, c in enumerate(courses, 1):
        print(f"{i}. {c.get('title', 'No title')}")
    
    client.close()

if __name__ == '__main__':
    asyncio.run(check_courses())
