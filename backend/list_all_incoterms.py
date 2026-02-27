import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

# Find all courses with "incoterms" in title or description
courses = list(db.courses.find({
    "$or": [
        {"title": {"$regex": "incoterms", "$options": "i"}},
        {"description": {"$regex": "incoterms", "$options": "i"}}
    ]
}))

print(f"Found {len(courses)} Incoterms course(s):\n")

for i, course in enumerate(courses, 1):
    print(f"{i}. Title: {course['title']}")
    print(f"   ID: {course.get('id', 'N/A')}")
    print(f"   Category: {course.get('category', 'N/A')}")
    print(f"   Published: {course.get('published', False)}")
    print(f"   Description: {course.get('description', 'N/A')[:100]}...")
    
    # Get modules
    modules = list(db.modules.find({"course_id": course.get("id")}))
    print(f"   Modules: {len(modules)}")
    for module in modules:
        print(f"      - {module['title']} ({len(module.get('lessons', []))} lessons)")
    print()

client.close()
