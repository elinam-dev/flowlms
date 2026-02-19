import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def check_incoterms_with_images():
    # Find all courses that might be Incoterms related
    incoterms_courses = list(db.courses.find({
        "$or": [
            {"title": {"$regex": "incoterms", "$options": "i"}},
            {"title": {"$regex": "inco terms", "$options": "i"}},
            {"title": {"$regex": "commercial terms", "$options": "i"}},
            {"description": {"$regex": "incoterms", "$options": "i"}}
        ]
    }))
    
    print(f"Found {len(incoterms_courses)} Incoterms courses:")
    
    for course in incoterms_courses:
        modules = course.get('modules', [])
        total_lessons = 0
        has_images = False
        
        for module in modules:
            lessons = module.get('lessons', [])
            total_lessons += len(lessons)
            
            # Check for images in lessons
            for lesson in lessons:
                content = lesson.get('content', '')
                if 'img' in content or '.jpg' in content or '.png' in content or 'image' in content:
                    has_images = True
        
        print(f"- {course['title']}: {total_lessons} lessons, Has images: {has_images}")
        print(f"  ID: {course['_id']}")

if __name__ == "__main__":
    check_incoterms_with_images()