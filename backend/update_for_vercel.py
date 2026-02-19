import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def update_for_vercel():
    # Update Incoterms course URLs for Vercel deployment
    incoterms_course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    if incoterms_course:
        module = db.modules.find_one({"course_id": incoterms_course["id"]})
        if module:
            lessons = list(db.lessons.find({"module_id": module["id"]}))
            
            for lesson in lessons:
                slide_num = lesson["title"].split()[-1]
                
                # Use Railway backend URL for Vercel
                new_content = f'<div class="slide-content"><img src="https://flowlms-production.up.railway.app/api/uploads/images/incoterms{slide_num}.jpeg" alt="Incoterms Slide {slide_num}" style="width: 100%; max-width: 800px; height: auto; display: block; margin: 0 auto;" /></div>'
                
                db.lessons.update_one(
                    {"id": lesson["id"]},
                    {"$set": {"content": new_content}}
                )
            
            print(f"Updated {len(lessons)} lessons for Vercel deployment")

if __name__ == "__main__":
    update_for_vercel()