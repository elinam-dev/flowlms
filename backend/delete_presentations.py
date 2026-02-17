from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Find all Engineering category courses (presentations)
presentation_courses = list(db.courses.find({"category": "Engineering"}))

print(f"Found {len(presentation_courses)} presentation courses to delete:")
for course in presentation_courses:
    print(f"  - {course.get('title')} ({course.get('code')})")

# Delete each course and its related data
for course in presentation_courses:
    course_id = course.get('id')
    
    # Delete modules
    modules = list(db.modules.find({"course_id": course_id}))
    for module in modules:
        module_id = module.get('id')
        # Delete lessons
        db.lessons.delete_many({"module_id": module_id})
        # Delete quizzes
        db.quizzes.delete_many({"module_id": module_id})
    
    db.modules.delete_many({"course_id": course_id})
    
    # Delete progress records
    db.progress.delete_many({"course_id": course_id})
    
    # Delete the course
    db.courses.delete_one({"_id": course["_id"]})
    
    print(f"Deleted: {course.get('title')}")

print("\nAll presentation courses deleted!")

# Show remaining courses
remaining = list(db.courses.find({}, {"_id": 0, "title": 1, "category": 1}))
print(f"\nRemaining courses: {len(remaining)}")
for course in remaining:
    print(f"  - {course.get('title')} ({course.get('category')})")

client.close()
