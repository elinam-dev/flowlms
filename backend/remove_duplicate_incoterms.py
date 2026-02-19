import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME')]

# Find all Incoterms courses
courses = list(db.courses.find({"title": "Introduction to International Commercial Terms"}))

print(f"Found {len(courses)} Incoterms courses")

if len(courses) > 1:
    # Keep the one with lessons, delete the other
    for course in courses:
        lesson_count = db.lessons.count_documents({"course_id": course['id']})
        print(f"Course ID {course['id']}: {lesson_count} lessons")
    
    # Delete courses with 0 or 1 lesson (keep the one with 19)
    for course in courses:
        lesson_count = db.lessons.count_documents({"course_id": course['id']})
        if lesson_count < 19:
            db.lessons.delete_many({"course_id": course['id']})
            db.modules.delete_many({"course_id": course['id']})
            db.courses.delete_one({"id": course['id']})
            print(f"Deleted course with {lesson_count} lessons")
