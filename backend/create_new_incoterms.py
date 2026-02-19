import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def create_incoterms_course():
    course = {
        "title": "Introduction to International and Commercial Terms (Incoterms)",
        "description": "Learn about International Commercial Terms (Incoterms) used in international trade to define responsibilities between buyers and sellers.",
        "category": "required",
        "thumbnail": "/images/incoterms-thumbnail.jpg",
        "duration": "45 minutes",
        "level": "Beginner",
        "published": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "modules": [
            {
                "title": "Understanding Incoterms",
                "lessons": [
                    {
                        "title": "What are Incoterms?",
                        "content": "<h2>Introduction to Incoterms</h2><p>International Commercial Terms (Incoterms) are standardized trade terms published by the International Chamber of Commerce (ICC) that define the responsibilities of buyers and sellers in international transactions.</p>",
                        "duration": "15 minutes"
                    }
                ]
            }
        ]
    }
    
    result = db.courses.insert_one(course)
    print(f"Created course: {course['title']}")
    print(f"Course ID: {result.inserted_id}")

if __name__ == "__main__":
    create_incoterms_course()