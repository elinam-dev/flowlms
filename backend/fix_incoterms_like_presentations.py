import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def fix_incoterms_like_presentations():
    # First, check how presentation courses are structured
    presentation_course = db.courses.find_one({"title": {"$regex": "Pump|Valve", "$options": "i"}})
    
    if presentation_course:
        print("Found presentation course structure:")
        print(f"Title: {presentation_course['title']}")
        if 'modules' in presentation_course:
            print("Has embedded modules")
        else:
            print("Uses separate modules collection")
    
    # Delete the current Incoterms course completely
    result = db.courses.delete_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    print(f"Deleted existing course: {result.deleted_count}")
    
    # Create new course with proper structure like presentation courses
    course_id = "incoterms_2024"
    
    # Create the course document
    course_doc = {
        "id": course_id,
        "title": "Introduction to International and Commercial Terms (Incoterms)",
        "description": "Learn about International Commercial Terms (Incoterms) used in international trade.",
        "thumbnail": "/images/incoterms-thumbnail.jpg",
        "category": "required",
        "duration_hours": 1,
        "is_published": True,
        "course_type": "compulsory",
        "enrolled_users": [],
        "created_at": "2024-01-01T00:00:00Z"
    }
    
    db.courses.insert_one(course_doc)
    
    # Create module
    module_id = f"{course_id}_module_1"
    module_doc = {
        "id": module_id,
        "course_id": course_id,
        "title": "Incoterms Presentation",
        "description": "Complete Incoterms presentation slides",
        "order": 0
    }
    
    db.modules.insert_one(module_doc)
    
    # Create lessons with proper image paths
    for i in range(1, 20):
        lesson_doc = {
            "id": f"{module_id}_lesson_{i}",
            "module_id": module_id,
            "title": f"Incoterms Slide {i}",
            "content_type": "text",
            "content": f'<div class="slide-content"><img src="https://flowlms-backend-production.up.railway.app/uploads/images/incoterms{i}.jpeg" alt="Incoterms Slide {i}" style="width: 100%; max-width: 800px; height: auto; display: block; margin: 0 auto;" /></div>',
            "duration_minutes": 3,
            "order": i - 1
        }
        
        db.lessons.insert_one(lesson_doc)
    
    print(f"Created new Incoterms course with {19} lessons")
    print("Course ID:", course_id)

if __name__ == "__main__":
    fix_incoterms_like_presentations()