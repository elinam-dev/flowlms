from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Count total courses
total_courses = db.courses.count_documents({})
print(f"Total courses: {total_courses}")

# Count by type
compulsory = db.courses.count_documents({"type": "compulsory"})
optional = db.courses.count_documents({"type": "optional"})

print(f"\nBy Type:")
print(f"  Compulsory: {compulsory}")
print(f"  Optional: {optional}")

# Count by category
categories = db.courses.distinct("category")
print(f"\nBy Category:")
for category in categories:
    count = db.courses.count_documents({"category": category})
    print(f"  {category}: {count}")

# List all courses
print(f"\nAll Courses:")
courses = list(db.courses.find({}, {"_id": 0, "title": 1, "code": 1, "category": 1, "type": 1}))
for i, course in enumerate(courses, 1):
    print(f"{i}. {course.get('title')} ({course.get('code')})")
    print(f"   Category: {course.get('category')}, Type: {course.get('type')}")

client.close()
