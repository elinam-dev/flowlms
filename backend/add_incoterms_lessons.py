import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

# Find the Incoterms course
course = db.courses.find_one({"title": {"$regex": "incoterms", "$options": "i"}})

if not course:
    print("Incoterms course not found")
    exit()

print(f"Found course: {course['title']}")

# Find the module
module = db.modules.find_one({"course_id": course["id"]})

if not module:
    print("No module found")
    exit()

print(f"Found module: {module['title']}")

# Create lessons for all 86 images
lessons = []
for i in range(1, 87):
    lesson = {
        "id": f"incoterms_2024_lesson_{i}",
        "title": f"Incoterms Slide {i}",
        "content": f'<div style="text-align: center;"><img src="/uploads/images/incoterms/incoterms{i}.jpeg" alt="Incoterms Slide {i}" style="max-width: 100%; height: auto;" /></div>',
        "duration": "2 minutes",
        "order": i
    }
    lessons.append(lesson)

# Update the module with all lessons
db.modules.update_one(
    {"_id": module["_id"]},
    {"$set": {"lessons": lessons}}
)

print(f"\nAdded {len(lessons)} lessons to the Incoterms course")
client.close()
