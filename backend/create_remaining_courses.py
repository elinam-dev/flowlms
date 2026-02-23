import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def create_remaining_courses():
    courses_data = {
        "personal_branding": [
            "Diploma in personal development skills",
            "Workplace communication Basics",
            "Effective B2B communication",
            "Emotional resilience at work",
            "Motivation - Power Guide to motivating yourself and others"
        ],
        "french": [
            "Diploma in French language studies"
        ]
    }
    
    created_count = 0
    
    for category, course_titles in courses_data.items():
        for title in course_titles:
            # Skip if course already exists
            existing = db.courses.find_one({"title": title})
            if existing:
                print(f"Skipping existing course: {title}")
                continue
                
            course_id = str(uuid.uuid4())
            
            # Create course
            course_doc = {
                "id": course_id,
                "title": title,
                "description": f"Professional training course in {title.lower()}",
                "thumbnail": "/images/course-thumbnail.jpg",
                "category": category,
                "duration_hours": 2,
                "is_published": True,
                "course_type": "optional",
                "enrolled_users": [],
                "created_at": datetime.now().isoformat()
            }
            
            db.courses.insert_one(course_doc)
            
            # Create module
            module_id = f"{course_id}_module_1"
            module_doc = {
                "id": module_id,
                "course_id": course_id,
                "title": "Course Content",
                "description": f"Main content for {title}",
                "order": 0
            }
            
            db.modules.insert_one(module_doc)
            
            # Create basic lesson
            lesson_doc = {
                "id": f"{module_id}_lesson_1",
                "module_id": module_id,
                "title": "Introduction",
                "content_type": "text",
                "content": f'<div class="lesson-content"><h2>{title}</h2><p>Welcome to this comprehensive course on {title.lower()}. This course will provide you with essential knowledge and skills.</p></div>',
                "duration_minutes": 30,
                "order": 0
            }
            
            db.lessons.insert_one(lesson_doc)
            created_count += 1
    
    print(f"Created {created_count} additional courses")

if __name__ == "__main__":
    create_remaining_courses()