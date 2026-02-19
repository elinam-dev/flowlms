import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def check_all_courses_for_incoterms():
    all_courses = list(db.courses.find({}))
    
    print(f"Checking {len(all_courses)} courses for Incoterms content...")
    
    for course in all_courses:
        title = course.get('title', '').lower()
        description = course.get('description', '').lower()
        
        # Check if course might be Incoterms related
        if any(term in title or term in description for term in ['inco', 'commercial', 'terms', 'trade']):
            modules = course.get('modules', [])
            total_lessons = 0
            has_images = False
            
            for module in modules:
                lessons = module.get('lessons', [])
                total_lessons += len(lessons)
                
                for lesson in lessons:
                    content = lesson.get('content', '')
                    if any(img_term in content.lower() for img_term in ['img', '.jpg', '.png', 'image', 'src=']):
                        has_images = True
            
            print(f"- {course['title']}: {total_lessons} lessons, Has images: {has_images}")

if __name__ == "__main__":
    check_all_courses_for_incoterms()