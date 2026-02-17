from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Update all courses with category "Compliance" to "Required"
result = db.courses.update_many(
    {"category": "Compliance"},
    {"$set": {"category": "Required"}}
)

print(f"Updated {result.modified_count} courses from 'Compliance' to 'Required'")

# Verify
courses = list(db.courses.find({}, {"_id": 0, "title": 1, "category": 1, "type": 1}))
print("\nAll courses:")
for course in courses:
    print(f"- {course.get('title')}: {course.get('category')} ({course.get('type')})")

client.close()
