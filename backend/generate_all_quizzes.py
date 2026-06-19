"""
AI Quiz Generator for LMS
Generates quizzes for all courses automatically
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import random
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Quiz templates for different course categories
QUIZ_TEMPLATES = {
    "Finance": {
        "accounting": [
            {
                "question": "What is the fundamental accounting equation?",
                "options": [
                    "Assets = Liabilities + Equity",
                    "Revenue - Expenses = Net Income",
                    "Debits = Credits",
                    "Assets + Liabilities = Equity"
                ],
                "correctAnswer": 0,
                "explanation": "The accounting equation (Assets = Liabilities + Equity) is the foundation of double-entry bookkeeping."
            },
            {
                "question": "Which financial statement shows a company's financial position at a specific point in time?",
                "options": [
                    "Balance Sheet",
                    "Income Statement",
                    "Cash Flow Statement",
                    "Statement of Retained Earnings"
                ],
                "correctAnswer": 0,
                "explanation": "The Balance Sheet provides a snapshot of assets, liabilities, and equity at a specific date."
            },
            {
                "question": "Depreciation is an example of which type of expense?",
                "options": [
                    "Non-cash expense",
                    "Variable expense",
                    "Direct expense",
                    "Discretionary expense"
                ],
                "correctAnswer": 0,
                "explanation": "Depreciation is a non-cash expense that allocates the cost of tangible assets over their useful lives."
            }
        ]
    },
    "HR": {
        "management": [
            {
                "question": "What is the primary purpose of performance management?",
                "options": [
                    "To improve employee performance and organizational effectiveness",
                    "To terminate underperforming employees",
                    "To reduce labor costs",
                    "To comply with legal requirements"
                ],
                "correctAnswer": 0,
                "explanation": "Performance management aims to align individual performance with organizational goals and foster continuous improvement."
            },
            {
                "question": "Which recruitment method typically has the lowest cost per hire?",
                "options": [
                    "Employee referrals",
                    "External recruitment agencies",
                    "Job advertisements",
                    "Campus recruitment"
                ],
                "correctAnswer": 0,
                "explanation": "Employee referrals are often the most cost-effective recruitment method and yield high-quality candidates."
            }
        ]
    },
    "Supply Chain": {
        "logistics": [
            {
                "question": "What does FOB (Free on Board) mean in shipping terms?",
                "options": [
                    "The seller is responsible until goods are loaded on the vessel",
                    "The buyer pays all shipping costs",
                    "Insurance is included in the price",
                    "Goods are delivered to the buyer's warehouse"
                ],
                "correctAnswer": 0,
                "explanation": "FOB means the seller's responsibility ends when goods are loaded onto the shipping vessel."
            },
            {
                "question": "What is the primary goal of supply chain management?",
                "options": [
                    "To optimize the flow of goods, information, and finances",
                    "To minimize inventory costs only",
                    "To reduce supplier relationships",
                    "To increase warehouse space"
                ],
                "correctAnswer": 0,
                "explanation": "Supply chain management aims to create value by optimizing the entire chain from suppliers to customers."
            }
        ]
    }
}

def generate_generic_questions(course_title, category, total_questions=18):
    """Generate generic but relevant questions based on course title and category"""
    questions = []
    base_id = 1
    
    # Common question templates
    templates = [
        {
            "question": f"What is the primary objective of {course_title}?",
            "options": [
                "To develop practical skills and theoretical knowledge in the field",
                "To memorize facts without application",
                "To replace hands-on experience",
                "To avoid real-world challenges"
            ],
            "correctAnswer": 0,
            "explanation": f"{course_title} aims to build both theoretical understanding and practical application skills."
        },
        {
            "question": f"Which of the following is a key principle covered in {course_title}?",
            "options": [
                "Understanding fundamental concepts and their applications",
                "Ignoring industry best practices",
                "Focusing only on theory without practice",
                "Avoiding standard methodologies"
            ],
            "correctAnswer": 0,
            "explanation": "This course emphasizes understanding core principles and applying them effectively."
        },
        {
            "question": "True or False: Continuous learning is essential for professional development in this field.",
            "options": [
                "True",
                "False",
                "Only for beginners",
                "Only for advanced practitioners"
            ],
            "correctAnswer": 0,
            "explanation": "Continuous learning keeps professionals updated with evolving practices and technologies."
        },
        {
            "question": "What is considered best practice when applying concepts from this course?",
            "options": [
                "Following established frameworks while adapting to specific contexts",
                "Using outdated methods",
                "Ignoring organizational requirements",
                "Applying one-size-fits-all solutions"
            ],
            "correctAnswer": 0,
            "explanation": "Best practices involve using proven frameworks while considering unique organizational needs."
        },
        {
            "question": "Which approach is most effective for implementing learning from this course?",
            "options": [
                "Practice with real-world scenarios and continuous improvement",
                "Theoretical study without application",
                "One-time implementation without review",
                "Avoiding feedback and adjustment"
            ],
            "correctAnswer": 0,
            "explanation": "Effective learning requires practical application, feedback, and iterative improvement."
        }
    ]
    
    # Add category-specific questions if available
    category_questions = []
    if category in QUIZ_TEMPLATES:
        for subcategory in QUIZ_TEMPLATES[category].values():
            category_questions.extend(subcategory)
    
    # Combine generic and specific questions
    all_questions = templates + category_questions
    random.shuffle(all_questions)
    
    # Select questions up to the limit
    selected = all_questions[:total_questions]
    
    for idx, q in enumerate(selected, 1):
        questions.append({
            "id": idx,
            "type": "multiple_choice",
            "question": q["question"],
            "options": q["options"],
            "correctAnswer": q["correctAnswer"],
            "explanation": q["explanation"]
        })
    
    return questions

async def generate_quiz_for_course(course, db):
    """Generate a quiz for a specific course"""
    course_id = course['id']
    course_title = course['title']
    category = course.get('category', 'General')
    
    print(f"Generating quiz for: {course_title}")
    
    # Find the module for this course
    module = await db.modules.find_one({"course_id": course_id})
    if not module:
        print(f"  [WARN] No module found for {course_title}")
        return None
    
    # Generate questions
    num_questions = random.randint(15, 20)
    questions = generate_generic_questions(course_title, category, num_questions)
    
    # Create quiz document
    quiz_id = f"quiz_{course_id}"
    quiz = {
        "id": quiz_id,
        "module_id": module['id'],
        "course_id": course_id,
        "title": f"{course_title} - Assessment",
        "description": f"Comprehensive assessment covering key concepts from {course_title}",
        "questions": questions,
        "passingScore": 70,
        "timeLimit": num_questions * 2,  # 2 minutes per question
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    # Insert into database
    await db.quizzes.insert_one(quiz)
    print(f"  [OK] Generated {num_questions} questions")
    
    return quiz

async def generate_all_quizzes():
    """Generate quizzes for all courses"""
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Get all courses
    courses = await db.courses.find({}).to_list(None)
    print(f"Found {len(courses)} courses\n")
    
    generated = 0
    skipped = 0
    
    for course in courses:
        try:
            quiz = await generate_quiz_for_course(course, db)
            if quiz:
                generated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  [ERROR] Error: {str(e)}")
            skipped += 1
    
    print(f"\n{'='*60}")
    print(f"[SUCCESS] Successfully generated: {generated} quizzes")
    print(f"[WARN] Skipped: {skipped} courses")
    print(f"{'='*60}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(generate_all_quizzes())
