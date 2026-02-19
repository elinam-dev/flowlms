from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Rename courses
updates = [
    {
        "old_title": "Presentation On Pump Spares",
        "new_title": "Pumps and Pump Spares"
    },
    {
        "old_title": "Valve Presentation",
        "new_title": "Valves"
    }
]

for update in updates:
    result = db.courses.update_one(
        {"title": update["old_title"]},
        {"$set": {"title": update["new_title"]}}
    )
    
    if result.modified_count > 0:
        print(f"Renamed: {update['old_title']} -> {update['new_title']}")
    else:
        print(f"Not found: {update['old_title']}")

print("\nAll courses:")
courses = list(db.courses.find({}, {"_id": 0, "title": 1, "category": 1}))
for course in courses:
    print(f"  - {course.get('title')} ({course.get('category')})")

client.close()
