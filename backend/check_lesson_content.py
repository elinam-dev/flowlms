import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

course = db.courses.find_one({"title": {"$regex": "incoterms", "$options": "i"}})
module = db.modules.find_one({"course_id": course["id"]})

print(f"Module has {len(module['lessons'])} lessons")
print("\nFirst 3 lessons:")
for i, lesson in enumerate(module['lessons'][:3], 1):
    print(f"\n{i}. {lesson['title']}")
    print(f"   Content: {lesson['content'][:150]}...")

client.close()
