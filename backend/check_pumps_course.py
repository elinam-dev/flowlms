from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Find the Pumps Spares course
pumps_course = db.courses.find_one({"code": "ENG-PUMPS-001"})

if pumps_course:
    print("Found Pumps Spares Presentation:")
    print(f"  Title: {pumps_course.get('title')}")
    print(f"  Code: {pumps_course.get('code')}")
    print(f"  is_published: {pumps_course.get('is_published')}")
    print(f"  Has 'id' field: {pumps_course.get('id', 'NO')}")
    print(f"  Has modules: {pumps_course.get('modules', 'NO')}")
    
    # Check if it has modules array
    if 'modules' in pumps_course:
        print(f"\n  Number of modules: {len(pumps_course['modules'])}")
        for i, module in enumerate(pumps_course['modules']):
            print(f"    Module {i+1}: {module.get('title')}")
            print(f"      Lessons: {len(module.get('lessons', []))}")
else:
    print("Pumps Spares Presentation NOT FOUND!")

# Check all courses
print("\n\nAll courses in database:")
all_courses = list(db.courses.find({}, {"_id": 0, "title": 1, "code": 1, "is_published": 1, "id": 1}))
for course in all_courses:
    print(f"- {course.get('title')} ({course.get('code')})")
    print(f"  Published: {course.get('is_published')}, Has ID: {'Yes' if course.get('id') else 'No'}")

client.close()
