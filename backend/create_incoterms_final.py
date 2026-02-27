import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

course_id = "incoterms_2024"

course = {
    "id": course_id,
    "title": "Introduction to Commercial Terms (Incoterms)",
    "description": "Learn about International Commercial Terms (Incoterms) used in international trade.",
    "category": "supply_chain",
    "thumbnail": "/images/incoterms-thumbnail.jpg",
    "duration": "3 hours",
    "level": "Intermediate",
    "published": True,
    "created_at": datetime.now(timezone.utc),
    "updated_at": datetime.now(timezone.utc)
}

db.courses.insert_one(course)
print(f"Created course: {course['title']}")

module = {
    "id": f"{course_id}_module_1",
    "course_id": course_id,
    "title": "Incoterms Presentation",
    "description": "Complete Incoterms presentation slides",
    "order": 0,
    "lessons": []
}

db.modules.insert_one(module)
print(f"Created module: {module['title']} (0 lessons)")

client.close()
