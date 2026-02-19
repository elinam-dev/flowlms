import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def fix_course_visibility():
    # Update the course to ensure it's visible
    result = db.courses.update_one(
        {"title": "Introduction to International and Commercial Terms (Incoterms)"},
        {
            "$set": {
                "published": True,
                "category": "required",
                "visibility": "public"
            }
        }
    )
    
    print(f"Course update result: {result.modified_count} documents modified")
    
    # Check if there are any users
    users = list(db.users.find({}, {"email": 1, "employee_id": 1, "role": 1}))
    print(f"\nFound {len(users)} users:")
    for user in users:
        print(f"- {user.get('email', user.get('employee_id', 'Unknown'))}: {user.get('role', 'N/A')}")

if __name__ == "__main__":
    fix_course_visibility()