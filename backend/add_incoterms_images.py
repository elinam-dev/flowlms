import os
from pymongo import MongoClient
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME')]

# Get the course and module
course = db.courses.find_one({"title": "Introduction to International Commercial Terms"})
module = db.modules.find_one({"course_id": course['id']})

# Delete existing lessons
db.lessons.delete_many({"module_id": module['id']})

# Create lessons for each image
for i in range(1, 20):
    lesson = {
        "id": str(uuid.uuid4()),
        "module_id": module['id'],
        "course_id": course['id'],
        "title": f"Incoterms - Slide {i}",
        "content": f'<div style="text-align: center;"><img src="/uploads/images/incoterms{i}.jpeg" alt="Incoterms Slide {i}" style="max-width: 100%; height: auto;" /></div>',
        "order": i,
        "duration": 5,
        "created_at": datetime.now()
    }
    db.lessons.insert_one(lesson)

print(f"Created 19 lessons with images for Incoterms course")
