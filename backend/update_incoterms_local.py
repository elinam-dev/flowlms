import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def update_incoterms_local():
    # Update Incoterms course with local URLs for 15 images
    incoterms_course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    if incoterms_course:
        module = db.modules.find_one({"course_id": incoterms_course["id"]})
        if module:
            # Delete existing lessons
            db.lessons.delete_many({"module_id": module["id"]})
            
            # Create new lessons for 15 images
            for i in range(1, 16):
                lesson_doc = {
                    "id": f"{module['id']}_lesson_{i}",
                    "module_id": module["id"],
                    "title": f"Incoterms Slide {i}",
                    "content_type": "text",
                    "content": f'<div class="slide-content"><img src="/api/uploads/images/incoterms{i}.jpeg" alt="Incoterms Slide {i}" style="width: 100%; max-width: 800px; height: auto; display: block; margin: 0 auto;" /></div>',
                    "duration_minutes": 3,
                    "order": i - 1
                }
                db.lessons.insert_one(lesson_doc)
            
            print(f"Updated Incoterms course with 15 lessons using local URLs")

if __name__ == "__main__":
    update_incoterms_local()