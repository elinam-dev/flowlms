import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

# Delete modules
modules_deleted = db.modules.delete_many({"course_id": "incoterms_2024"})
print(f"Deleted {modules_deleted.deleted_count} modules")

# Delete progress
progress_deleted = db.progress.delete_many({"course_id": "incoterms_2024"})
print(f"Deleted {progress_deleted.deleted_count} progress records")

# Delete course
course_deleted = db.courses.delete_one({"id": "incoterms_2024"})
print(f"Deleted {course_deleted.deleted_count} course")

print("\nIncoterms course completely deleted")
client.close()
