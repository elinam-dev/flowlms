import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def delete_incoterms_lessons():
    # Find the Incoterms course
    course = db.courses.find_one({
        "$or": [
            {"title": {"$regex": "incoterms", "$options": "i"}},
            {"description": {"$regex": "incoterms", "$options": "i"}}
        ]
    })
    
    if not course:
        print("No Incoterms course found")
        return
    
    print(f"Found course: {course['title']}")
    
    # Find all modules for this course
    modules = list(db.modules.find({"course_id": course["id"]}))
    
    total_deleted = 0
    for module in modules:
        lessons = module.get("lessons", [])
        print(f"Module '{module['title']}' has {len(lessons)} lessons")
        total_deleted += len(lessons)
        
        # Clear all lessons from the module
        db.modules.update_one(
            {"_id": module["_id"]},
            {"$set": {"lessons": []}}
        )
    
    print(f"\nDeleted {total_deleted} lessons from Incoterms course")
    client.close()

if __name__ == "__main__":
    delete_incoterms_lessons()
