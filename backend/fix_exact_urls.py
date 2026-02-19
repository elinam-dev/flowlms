import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def fix_exact_urls():
    # Get exact working URL from pump course
    pump_module = db.modules.find_one({"course_id": {"$regex": "pump_curves"}})
    if pump_module:
        pump_lesson = db.lessons.find_one({"module_id": pump_module["id"]})
        if pump_lesson:
            content = pump_lesson["content"]
            print("Working pump lesson content:")
            print(content[:200] + "...")
            
            # Extract the exact URL pattern
            if 'src="' in content:
                start = content.find('src="') + 5
                end = content.find('"', start)
                working_url = content[start:end]
                print(f"Working URL: {working_url}")
                
                # Get the base URL
                base_url = working_url.split('/uploads/')[0]
                print(f"Base URL: {base_url}")
    
    # Update Incoterms with exact same format
    incoterms_course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    if incoterms_course:
        module = db.modules.find_one({"course_id": incoterms_course["id"]})
        if module:
            lessons = list(db.lessons.find({"module_id": module["id"]}))
            
            for lesson in lessons:
                slide_num = lesson["title"].split()[-1]
                
                # Use exact same format as working courses
                new_content = f'<div class="slide-content"><img src="https://flowlms-production.up.railway.app/uploads/images/incoterms{slide_num}.jpeg" alt="Incoterms Slide {slide_num}" style="width: 100%; max-width: 800px; height: auto; display: block; margin: 0 auto;" /></div>'
                
                db.lessons.update_one(
                    {"id": lesson["id"]},
                    {"$set": {"content": new_content}}
                )
            
            print(f"Updated {len(lessons)} lessons with exact URL format")

if __name__ == "__main__":
    fix_exact_urls()