import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

# Count total courses
total = db.courses.count_documents({})
print(f"Total courses in database: {total}")

# Count published courses
published = db.courses.count_documents({"is_published": True})
print(f"Published courses: {published}")

# Count unpublished courses
unpublished = db.courses.count_documents({"is_published": False})
print(f"Unpublished courses: {unpublished}")

# Check if any courses are missing is_published field
no_field = db.courses.count_documents({"is_published": {"$exists": False}})
print(f"Courses without is_published field: {no_field}")

client.close()
