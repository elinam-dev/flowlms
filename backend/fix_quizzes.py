"""
Add quizzes to courses that don't have them
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def fix_missing_quizzes():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Checking for courses without quizzes...")
    
    courses = await db.courses.find({}).to_list(1000)
    fixed_count = 0
    
    for course in courses:
        modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
        if not modules:
            continue
        
        module = modules[0]
        
        # Check if quiz exists
        existing_quiz = await db.quizzes.find_one({"module_id": module["id"]})
        if existing_quiz:
            continue
        
        # Add quiz
        quiz_id = str(uuid.uuid4())
        questions = generate_quiz_questions(course.get('category', 'General'))
        
        await db.quizzes.insert_one({
            "id": quiz_id,
            "module_id": module["id"],
            "title": f"{course['title']} - Final Assessment",
            "description": f"Test your knowledge of {course['title']}. You need 70% to pass.",
            "passing_score": 70,
            "questions": questions,
            "time_limit_minutes": 24,
            "created_at": "2024-01-01T00:00:00"
        })
        
        fixed_count += 1
        print(f"  ✓ Added quiz to: {course['title']}")
    
    print(f"\n✅ Added {fixed_count} missing quizzes!")
    client.close()

def generate_quiz_questions(category):
    return [
        {"question": f"What is a key principle in {category}?", "question_type": "multiple_choice", "options": ["Ignore standards", "Follow best practices", "Avoid learning", "Skip training"], "correct_answer": "Follow best practices", "points": 1, "order": 0},
        {"question": "Continuous improvement is essential for success.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 1},
        {"question": "What drives professional excellence?", "question_type": "multiple_choice", "options": ["Avoiding work", "Applying knowledge", "Ignoring feedback", "Staying static"], "correct_answer": "Applying knowledge", "points": 1, "order": 2},
        {"question": "Quality standards should be followed consistently.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 3},
        {"question": "What is essential for team success?", "question_type": "multiple_choice", "options": ["Working alone", "Collaboration", "Avoiding communication", "Ignoring goals"], "correct_answer": "Collaboration", "points": 1, "order": 4},
        {"question": "Safety is a priority in all operations.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 5},
        {"question": "What ensures quality outcomes?", "question_type": "multiple_choice", "options": ["Rushing work", "Following procedures", "Skipping checks", "Ignoring details"], "correct_answer": "Following procedures", "points": 1, "order": 6},
        {"question": "Professional development requires ongoing effort.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 7},
        {"question": "What is key to problem solving?", "question_type": "multiple_choice", "options": ["Ignoring issues", "Systematic analysis", "Avoiding decisions", "Guessing solutions"], "correct_answer": "Systematic analysis", "points": 1, "order": 8},
        {"question": "Effective communication improves team performance.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 9},
        {"question": "What drives organizational success?", "question_type": "multiple_choice", "options": ["Avoiding change", "Excellence and innovation", "Maintaining status quo", "Ignoring customers"], "correct_answer": "Excellence and innovation", "points": 1, "order": 10},
        {"question": "Accountability is essential for professional success.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 11}
    ]

if __name__ == "__main__":
    asyncio.run(fix_missing_quizzes())
