from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Update all courses to set is_published = True
result = db.courses.update_many(
    {},
    {"$set": {"is_published": True}}
)

print(f"Updated {result.modified_count} courses to published status")

# Verify
courses = list(db.courses.find({}, {"_id": 0, "title": 1, "is_published": 1}))
print("\nAll courses:")
for course in courses:
    print(f"- {course.get('title')}: is_published = {course.get('is_published')}")

client.close()
