import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def fix_incoterms_structure():
    # Find the Incoterms course
    course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    
    if not course:
        print("Course not found!")
        return
    
    # Fix the course structure to match what the frontend expects
    fixed_modules = []
    
    for module in course.get('modules', []):
        fixed_lessons = []
        
        for lesson in module.get('lessons', []):
            # Ensure all lesson fields are strings, not objects
            fixed_lesson = {
                "title": str(lesson.get('title', '')),
                "content": str(lesson.get('content', '')),
                "duration": str(lesson.get('duration', '3 minutes'))
            }
            fixed_lessons.append(fixed_lesson)
        
        fixed_module = {
            "title": str(module.get('title', '')),
            "lessons": fixed_lessons
        }
        fixed_modules.append(fixed_module)
    
    # Update the course
    db.courses.update_one(
        {"_id": course["_id"]},
        {
            "$set": {
                "modules": fixed_modules,
                "duration": "57 minutes"
            }
        }
    )
    
    print(f"Fixed course structure with {len(fixed_modules)} modules")
    if fixed_modules:
        print(f"First module has {len(fixed_modules[0]['lessons'])} lessons")

if __name__ == "__main__":
    fix_incoterms_structure()