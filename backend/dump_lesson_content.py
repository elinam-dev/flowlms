import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

course = db.courses.find_one({"id": "incoterms_2024"})
module = db.modules.find_one({"course_id": "incoterms_2024"})

print(f"Course: {course['title']}")
print(f"Module: {module['title']}")
print(f"Total lessons: {len(module['lessons'])}\n")

print("First 5 lessons content:")
for i, lesson in enumerate(module['lessons'][:5], 1):
    print(f"\n{i}. {lesson['title']}")
    print(f"   Full content: {lesson['content']}")

client.close()
