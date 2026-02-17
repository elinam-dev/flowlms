from pymongo import MongoClient
import os
import uuid
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Get the Pumps course
pumps_course = db.courses.find_one({"code": "ENG-PUMPS-001"})

if pumps_course and 'modules' in pumps_course:
    print("Restructuring Pumps Spares Presentation...")
    
    # Extract embedded modules
    embedded_modules = pumps_course['modules']
    
    # Create separate module and lesson documents
    for module_data in embedded_modules:
        module_id = str(uuid.uuid4())
        
        # Create module document
        module_doc = {
            "id": module_id,
            "course_id": pumps_course['id'],
            "title": module_data['title'],
            "description": "",
            "order": module_data.get('order', 0)
        }
        db.modules.insert_one(module_doc)
        print(f"Created module: {module_data['title']}")
        
        # Create lesson documents
        for lesson_data in module_data.get('lessons', []):
            lesson_id = str(uuid.uuid4())
            lesson_doc = {
                "id": lesson_id,
                "module_id": module_id,
                "title": lesson_data['title'],
                "content_type": lesson_data['type'],
                "content": lesson_data['content'],
                "duration_minutes": 10,
                "order": lesson_data.get('order', 0)
            }
            db.lessons.insert_one(lesson_doc)
            print(f"  Created lesson: {lesson_data['title']}")
    
    # Remove embedded modules from course
    db.courses.update_one(
        {"_id": pumps_course['_id']},
        {"$unset": {"modules": ""}}
    )
    print("\nRestructuring complete!")
else:
    print("Course not found or already restructured")

client.close()
