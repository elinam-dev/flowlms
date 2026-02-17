from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Check courses
courses = list(db.courses.find({}))
print(f"Total courses in database: {len(courses)}")
print("\nCourses:")
for course in courses:
    print(f"- {course.get('title')} (Code: {course.get('code')}, Type: {course.get('type')})")
    print(f"  ID: {course.get('_id')}")
    print(f"  Has 'id' field: {course.get('id', 'NO')}")
    print()

client.close()
