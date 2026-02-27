import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

total = db.courses.count_documents({})
print(f"Total courses in database: {total}")

# List all courses
courses = list(db.courses.find({}, {"_id": 0, "id": 1, "title": 1, "category": 1}))
print(f"\nAll {len(courses)} courses:")
for i, course in enumerate(courses, 1):
    print(f"{i}. {course.get('title')} (Category: {course.get('category', 'N/A')})")

client.close()
