from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Get all courses
all_courses = list(db.courses.find({}, {"_id": 0}))

print("All courses in database:\n")
for i, course in enumerate(all_courses, 1):
    print(f"{i}. {course.get('title')}")
    print(f"   Code: {course.get('code')}")
    print(f"   Category: {course.get('category')}")
    print(f"   Type: {course.get('type')}")
    print(f"   is_published: {course.get('is_published')}")
    print(f"   Has 'id': {bool(course.get('id'))}")
    print(f"   Duration: {course.get('duration')}")
    print()

# Check if Pumps course has same structure as others
pumps = db.courses.find_one({"code": "ENG-PUMPS-001"})
ethics = db.courses.find_one({"code": "FLGG/232/72/CEPC3"})

if pumps and ethics:
    print("\nComparing Pumps vs Ethics course structure:")
    print(f"Pumps keys: {set(pumps.keys())}")
    print(f"Ethics keys: {set(ethics.keys())}")
    print(f"\nMissing in Pumps: {set(ethics.keys()) - set(pumps.keys())}")
    print(f"Extra in Pumps: {set(pumps.keys()) - set(ethics.keys())}")

client.close()
