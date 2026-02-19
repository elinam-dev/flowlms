import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def add_incoterms_overview_image():
    # Find the Incoterms course
    incoterms_course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    if incoterms_course:
        module = db.modules.find_one({"course_id": incoterms_course["id"]})
        if module:
            # Find the first lesson (Course Overview)
            first_lesson = db.lessons.find_one({"module_id": module["id"], "order": 0})
            if first_lesson:
                # Add overview image to the first lesson
                new_content = '''<div class="lesson-content">
<div class="course-header-image">
<img src="https://flowlms-production.up.railway.app/api/uploads/images/incoterms1.jpeg" alt="Incoterms Course Overview" style="width: 100%; max-width: 800px; height: auto; display: block; margin: 0 auto 20px auto;" />
</div>
''' + first_lesson["content"][22:]  # Remove opening div tag to avoid duplication
                
                db.lessons.update_one(
                    {"id": first_lesson["id"]},
                    {"$set": {"content": new_content}}
                )
                
                print("Added overview image to Incoterms course")

if __name__ == "__main__":
    add_incoterms_overview_image()