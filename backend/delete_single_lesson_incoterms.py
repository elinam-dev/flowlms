import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def delete_single_lesson_incoterms():
    # Find all courses that might be Incoterms related
    incoterms_courses = list(db.courses.find({
        "$or": [
            {"title": {"$regex": "incoterms", "$options": "i"}},
            {"title": {"$regex": "inco terms", "$options": "i"}},
            {"title": {"$regex": "inco", "$options": "i"}},
            {"description": {"$regex": "incoterms", "$options": "i"}}
        ]
    }))
    
    # If no specific matches, let's check all courses for single lesson ones
    if not incoterms_courses:
        print("No Incoterms courses found, checking all courses with single lessons...")
        all_courses = list(db.courses.find({}))
        single_lesson_courses = []
        
        for course in all_courses:
            lesson_count = len(course.get('modules', [{}])[0].get('lessons', []))
            if lesson_count == 1:
                single_lesson_courses.append(course)
                print(f"Single lesson course: {course['title']}")
        
        incoterms_courses = single_lesson_courses
    
    print(f"Found {len(incoterms_courses)} potential courses:")
    
    for course in incoterms_courses:
        modules = course.get('modules', [])
        total_lessons = 0
        for module in modules:
            total_lessons += len(module.get('lessons', []))
        
        print(f"- {course['title']}: {total_lessons} lessons (ID: {course['_id']})")
        
        # Delete Incoterms courses (they seem to have issues)
        if "commercial terms" in course['title'].lower() or "inco" in course['title'].lower():
            print(f"Deleting Incoterms course: {course['title']}")
            result = db.courses.delete_one({"_id": course["_id"]})
            if result.deleted_count > 0:
                print(f"Successfully deleted course: {course['title']}")
            else:
                print(f"Failed to delete course: {course['title']}")

if __name__ == "__main__":
    delete_single_lesson_incoterms()