import os
from pymongo import MongoClient
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME')]

course_id = str(uuid.uuid4())
module_id = str(uuid.uuid4())

course = {
    "id": course_id,
    "title": "Introduction to International Commercial Terms",
    "description": "Learn about Incoterms and their application in international trade.",
    "category": "Required",
    "type": "compulsory",
    "duration": "2 hours",
    "thumbnail": "",
    "is_published": True,
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

module = {
    "id": module_id,
    "course_id": course_id,
    "title": "Incoterms Fundamentals",
    "description": "Understanding international commercial terms",
    "order": 1,
    "created_at": datetime.utcnow()
}

lesson = {
    "id": str(uuid.uuid4()),
    "module_id": module_id,
    "course_id": course_id,
    "title": "Introduction to Incoterms",
    "content": "<h2>What are Incoterms?</h2><p>Incoterms (International Commercial Terms) are standardized trade terms published by the International Chamber of Commerce (ICC).</p>",
    "order": 1,
    "duration": 10,
    "created_at": datetime.utcnow()
}

db.courses.insert_one(course)
db.modules.insert_one(module)
db.lessons.insert_one(lesson)

print(f"Created course: {course['title']}")
print(f"Course ID: {course_id}")
