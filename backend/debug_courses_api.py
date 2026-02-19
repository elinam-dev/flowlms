import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def debug_courses_api():
    # Check the exact structure the API expects
    print("=== Checking course structure ===")
    
    # Find the Incoterms course
    course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    
    if course:
        print(f"Course found: {course['title']}")
        print(f"Published field: {course.get('published', 'NOT SET')}")
        print(f"is_published field: {course.get('is_published', 'NOT SET')}")
        print(f"Category: {course.get('category', 'NOT SET')}")
        
        # The API expects 'is_published' field, let's fix this
        if 'published' in course and 'is_published' not in course:
            print("Fixing published field...")
            db.courses.update_one(
                {"_id": course["_id"]},
                {"$set": {"is_published": course['published']}}
            )
            print("Fixed!")
        
        # Also check if it has the right structure
        print(f"Has modules: {len(course.get('modules', []))}")
        
    # Check all courses that should be visible
    print("\n=== All published courses ===")
    published_courses = list(db.courses.find({"is_published": True}, {"title": 1, "is_published": 1, "category": 1}))
    for c in published_courses:
        print(f"- {c['title']} (Published: {c.get('is_published')}, Category: {c.get('category')})")

if __name__ == "__main__":
    debug_courses_api()