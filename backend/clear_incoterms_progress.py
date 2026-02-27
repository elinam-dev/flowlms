import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

# Clear all progress for Incoterms course
result = db.progress.delete_many({"course_id": "incoterms_2024"})
print(f"Deleted {result.deleted_count} progress records for Incoterms course")

# Update course to force refresh
db.courses.update_one(
    {"id": "incoterms_2024"},
    {"$set": {"updated_at": "2026-02-25T00:00:00Z"}}
)

print("Course updated - users will see fresh content")
client.close()
