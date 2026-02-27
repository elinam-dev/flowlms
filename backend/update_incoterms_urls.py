import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

# Find the Incoterms course
course = db.courses.find_one({"title": {"$regex": "incoterms", "$options": "i"}})
module = db.modules.find_one({"course_id": course["id"]})

# Update lessons with localhost URL
lessons = []
for i in range(1, 87):
    lesson = {
        "id": f"incoterms_2024_lesson_{i}",
        "title": f"Incoterms Slide {i}",
        "content": f'<div style="text-align: center;"><img src="http://localhost:8000/uploads/images/incoterms/incoterms{i}.jpeg?v={i}" alt="Incoterms Slide {i}" style="max-width: 100%; height: auto;" /></div>',
        "duration": "2 minutes",
        "order": i
    }
    lessons.append(lesson)

db.modules.update_one(
    {"_id": module["_id"]},
    {"$set": {"lessons": lessons}}
)

print(f"Updated {len(lessons)} lessons with localhost URLs and cache busting")
client.close()
