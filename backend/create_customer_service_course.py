import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def create_customer_service_course():
    course_id = "customer_service_skills_2024"
    
    # Create the course
    course_doc = {
        "id": course_id,
        "title": "Customer Service Skills",
        "description": "Essential skills for delivering exceptional customer service and building strong client relationships.",
        "thumbnail": "/images/customer-service-thumbnail.jpg",
        "category": "sales",
        "duration_hours": 3,
        "is_published": True,
        "course_type": "optional",
        "enrolled_users": [],
        "created_at": datetime.utcnow().isoformat()
    }
    
    db.courses.insert_one(course_doc)
    
    # Create module
    module_id = f"{course_id}_module_1"
    module_doc = {
        "id": module_id,
        "course_id": course_id,
        "title": "Customer Service Fundamentals",
        "description": "Core principles and skills for excellent customer service",
        "order": 0
    }
    
    db.modules.insert_one(module_doc)
    
    # Create lessons
    lessons = [
        {
            "title": "Introduction to Customer Service",
            "content": '<div class="lesson-content"><h2>Welcome to Customer Service Skills</h2><p>Learn the fundamentals of delivering exceptional customer service that builds loyalty and drives business success.</p></div>'
        },
        {
            "title": "Understanding Customer Needs",
            "content": '<div class="lesson-content"><h2>Understanding Customer Needs</h2><p>Discover how to identify, understand, and anticipate what your customers truly need.</p></div>'
        },
        {
            "title": "Communication Excellence",
            "content": '<div class="lesson-content"><h2>Communication Excellence</h2><p>Master the art of clear, empathetic, and effective communication with customers.</p></div>'
        },
        {
            "title": "Handling Difficult Situations",
            "content": '<div class="lesson-content"><h2>Handling Difficult Situations</h2><p>Learn strategies for managing challenging customer interactions and turning complaints into opportunities.</p></div>'
        },
        {
            "title": "Building Customer Loyalty",
            "content": '<div class="lesson-content"><h2>Building Customer Loyalty</h2><p>Understand how to create lasting relationships that keep customers coming back.</p></div>'
        }
    ]
    
    for i, lesson_data in enumerate(lessons):
        lesson_doc = {
            "id": f"{module_id}_lesson_{i+1}",
            "module_id": module_id,
            "title": lesson_data["title"],
            "content_type": "text",
            "content": lesson_data["content"],
            "duration_minutes": 30,
            "order": i
        }
        db.lessons.insert_one(lesson_doc)
    
    print(f"Created Customer Service Skills course with {len(lessons)} lessons")
    print(f"Course ID: {course_id}")

if __name__ == "__main__":
    create_customer_service_course()