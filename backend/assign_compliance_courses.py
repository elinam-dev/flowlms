from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Get the 4 compliance courses by their codes
course_codes = ["FLGG/232/72/CEPC3", "DCPC/HR1", "LPHR1", "H/SP1"]
courses = list(db.courses.find({"code": {"$in": course_codes}}))

if len(courses) != 4:
    print(f"Error: Expected 4 courses, found {len(courses)}")
    client.close()
    exit(1)

course_ids = [str(course["_id"]) for course in courses]
print(f"Found courses: {[c['title'] for c in courses]}")

# Get all users
users = list(db.users.find({}))
print(f"Found {len(users)} users")

# Assign courses to each user
assigned_count = 0
for user in users:
    user_id = str(user["_id"])
    
    # Check existing enrollments
    existing_enrollments = list(db.enrollments.find({
        "userId": user_id,
        "courseId": {"$in": course_ids}
    }))
    
    existing_course_ids = [e["courseId"] for e in existing_enrollments]
    
    # Add missing enrollments
    for course_id in course_ids:
        if course_id not in existing_course_ids:
            enrollment = {
                "userId": user_id,
                "courseId": course_id,
                "status": "not_started",
                "progress": 0,
                "enrolledAt": None
            }
            db.enrollments.insert_one(enrollment)
            assigned_count += 1

print(f"Assigned {assigned_count} new course enrollments")
print("All users now have access to the 4 compliance courses")

client.close()
