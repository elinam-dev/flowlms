from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Get all Engineering courses (presentations)
presentation_courses = list(db.courses.find({"category": "Engineering"}))

print(f"Found {len(presentation_courses)} presentation courses\n")

for course in presentation_courses:
    course_id = course.get('id')
    course_title = course.get('title')
    
    print(f"Processing: {course_title}")
    
    # Get the module
    module = db.modules.find_one({"course_id": course_id})
    
    if module:
        module_id = module.get('id')
        
        # Get all lessons sorted by order
        lessons = list(db.lessons.find({"module_id": module_id}).sort("order", 1))
        total_lessons = len(lessons)
        
        if total_lessons > 0:
            # Get the last lesson
            last_lesson = lessons[-1]
            
            # Delete the last lesson
            db.lessons.delete_one({"_id": last_lesson["_id"]})
            
            print(f"  Removed last slide: {last_lesson.get('title')}")
            print(f"  Lessons: {total_lessons} -> {total_lessons - 1}")
        else:
            print(f"  No lessons found")
    else:
        print(f"  No module found")
    
    print()

print("✓ Removed last slide from all presentation courses!")

client.close()
