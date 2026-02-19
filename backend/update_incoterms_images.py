import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def update_incoterms_with_images():
    # Find the Incoterms course
    course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    
    if not course:
        print("Incoterms course not found!")
        return
    
    # Create lessons with images
    lessons = []
    for i in range(1, 20):  # incoterms1.jpeg to incoterms19.jpeg
        lesson = {
            "title": f"Incoterms Slide {i}",
            "content": f'<div class="lesson-content"><img src="/uploads/images/incoterms{i}.jpeg" alt="Incoterms Slide {i}" style="width: 100%; max-width: 800px; height: auto;" /></div>',
            "duration": "3 minutes"
        }
        lessons.append(lesson)
    
    # Update the course with new lessons
    db.courses.update_one(
        {"_id": course["_id"]},
        {
            "$set": {
                "modules": [
                    {
                        "title": "Incoterms Presentation",
                        "lessons": lessons
                    }
                ],
                "duration": f"{len(lessons) * 3} minutes"
            }
        }
    )
    
    print(f"Updated Incoterms course with {len(lessons)} image lessons")

if __name__ == "__main__":
    update_incoterms_with_images()