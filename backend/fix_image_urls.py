import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def fix_image_urls():
    # Check how other courses reference images
    pump_course = db.courses.find_one({"title": {"$regex": "Pump", "$options": "i"}})
    if pump_course:
        # Get a lesson from this course to see image URL format
        module = db.modules.find_one({"course_id": pump_course["id"]})
        if module:
            lesson = db.lessons.find_one({"module_id": module["id"]})
            if lesson and "img src" in lesson.get("content", ""):
                print("Sample image URL from working course:")
                content = lesson["content"]
                start = content.find('src="') + 5
                end = content.find('"', start)
                sample_url = content[start:end]
                print(f"Sample URL: {sample_url}")
    
    # Update Incoterms lessons with correct image URLs
    incoterms_course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    if incoterms_course:
        module = db.modules.find_one({"course_id": incoterms_course["id"]})
        if module:
            lessons = db.lessons.find({"module_id": module["id"]})
            
            for lesson in lessons:
                # Extract slide number from title
                slide_num = lesson["title"].split()[-1]
                
                # Use the correct URL format
                new_content = f'<div class="slide-content"><img src="/uploads/images/incoterms{slide_num}.jpeg" alt="Incoterms Slide {slide_num}" style="width: 100%; max-width: 800px; height: auto; display: block; margin: 0 auto;" /></div>'
                
                db.lessons.update_one(
                    {"id": lesson["id"]},
                    {"$set": {"content": new_content}}
                )
            
            print("Updated all Incoterms lesson image URLs")

if __name__ == "__main__":
    fix_image_urls()