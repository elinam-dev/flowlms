import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

# Find the Incoterms course
course = db.courses.find_one({
    "$or": [
        {"title": {"$regex": "incoterms", "$options": "i"}},
        {"description": {"$regex": "incoterms", "$options": "i"}}
    ]
})

if course:
    print(f"Course: {course['title']}")
    print(f"Course ID: {course.get('id', 'N/A')}")
    print(f"Published: {course.get('published', False)}")
    print(f"\nModules:")
    
    modules = list(db.modules.find({"course_id": course.get("id")}))
    print(f"Found {len(modules)} modules")
    
    for i, module in enumerate(modules, 1):
        print(f"\n  Module {i}: {module['title']}")
        print(f"  Module ID: {module.get('id', 'N/A')}")
        lessons = module.get("lessons", [])
        print(f"  Lessons: {len(lessons)}")
        
        if lessons:
            for j, lesson in enumerate(lessons, 1):
                print(f"    {j}. {lesson.get('title', 'Untitled')}")
else:
    print("No Incoterms course found")

client.close()
