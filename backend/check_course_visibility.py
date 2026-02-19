import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def check_incoterms_course():
    # Find the Incoterms course
    course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    
    if course:
        print(f"Course found: {course['title']}")
        print(f"Published: {course.get('published', False)}")
        print(f"Category: {course.get('category', 'N/A')}")
        print(f"ID: {course['_id']}")
        print(f"Modules: {len(course.get('modules', []))}")
        if course.get('modules'):
            print(f"Lessons: {len(course['modules'][0].get('lessons', []))}")
    else:
        print("Course not found!")
        
    # Check all courses to see what's available
    all_courses = list(db.courses.find({}, {"title": 1, "published": 1, "category": 1}))
    print(f"\nAll courses ({len(all_courses)}):")
    for c in all_courses:
        print(f"- {c['title']} (Published: {c.get('published', False)}, Category: {c.get('category', 'N/A')})")

if __name__ == "__main__":
    check_incoterms_course()