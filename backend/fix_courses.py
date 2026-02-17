from pymongo import MongoClient
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Fix courses without 'id' field
courses_without_id = list(db.courses.find({"id": {"$exists": False}}))
print(f"Found {len(courses_without_id)} courses without 'id' field")

for course in courses_without_id:
    new_id = str(uuid.uuid4())
    db.courses.update_one(
        {"_id": course["_id"]},
        {"$set": {"id": new_id}}
    )
    print(f"Added id to: {course.get('title')}")

# Remove duplicate Pumps Spares Presentation (keep the latest one)
pumps_courses = list(db.courses.find({"code": "ENG-PUMPS-001"}).sort("createdAt", -1))
if len(pumps_courses) > 1:
    print(f"\nFound {len(pumps_courses)} duplicate Pumps Spares courses")
    # Keep the first (latest), delete the rest
    for course in pumps_courses[1:]:
        db.courses.delete_one({"_id": course["_id"]})
        print(f"Deleted duplicate: {course.get('_id')}")

print("\nFixed! Checking courses now:")
courses = list(db.courses.find({}))
print(f"\nTotal courses: {len(courses)}")
for course in courses:
    print(f"- {course.get('title')} (Code: {course.get('code')})")

client.close()
