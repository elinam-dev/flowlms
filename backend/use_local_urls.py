import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def use_local_urls():
    # Update to use local server URLs for testing
    incoterms_course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    if incoterms_course:
        module = db.modules.find_one({"course_id": incoterms_course["id"]})
        if module:
            lessons = list(db.lessons.find({"module_id": module["id"]}))
            
            for lesson in lessons:
                slide_num = lesson["title"].split()[-1]
                
                # Use local server URL format
                new_content = f'<div class="slide-content"><img src="http://localhost:8001/uploads/images/incoterms{slide_num}.jpeg" alt="Incoterms Slide {slide_num}" style="width: 100%; max-width: 800px; height: auto; display: block; margin: 0 auto;" /></div>'
                
                db.lessons.update_one(
                    {"id": lesson["id"]},
                    {"$set": {"content": new_content}}
                )
            
            print(f"Updated {len(lessons)} lessons with local URLs")

if __name__ == "__main__":
    use_local_urls()