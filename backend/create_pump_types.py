import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def create_course():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course_id = str(uuid.uuid4())
    module_id = str(uuid.uuid4())
    
    # Create course
    await db.courses.insert_one({
        "id": course_id,
        "title": "Pump Types, Parts & Working Principles",
        "code": "ENG-PUMP-003",
        "description": "Comprehensive training on different pump types, their components, and working principles.",
        "category": "Engineering",
        "level": "Intermediate",
        "duration": 80,
        "is_compulsory": False,
        "is_published": True,
        "thumbnail": "http://127.0.0.1:8000/api/uploads/images/pump_tyres_01.png"
    })
    
    # Create module
    await db.modules.insert_one({
        "id": module_id,
        "course_id": course_id,
        "title": "Pump Types, Parts & Working Principles",
        "description": "Complete presentation on pump types and components",
        "order": 1
    })
    
    # Create 27 lessons
    for i in range(1, 28):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": f"Slide {i}",
            "content_type": "text",
            "content": f'<div style="text-align: center;"><img src="http://127.0.0.1:8000/api/uploads/images/pump_tyres_{i:02d}.png" alt="Slide {i}" style="max-width: 100%; height: auto;" /></div>',
            "duration_minutes": 2,
            "order": i - 1
        })
    
    # Create quiz
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "course_id": course_id,
        "title": "Pump Types & Working Principles Assessment",
        "passing_score": 70,
        "questions": [
            {
                "question": "What are the two main categories of pumps?",
                "type": "multiple_choice",
                "options": ["Positive displacement and dynamic", "Centrifugal and axial", "Rotary and reciprocating", "Electric and manual"],
                "correct_answer": "Positive displacement and dynamic"
            },
            {
                "question": "Centrifugal pumps use rotating impellers to move fluid.",
                "type": "true_false",
                "correct_answer": "true"
            },
            {
                "question": "What is the main advantage of positive displacement pumps?",
                "type": "multiple_choice",
                "options": ["Low cost", "Constant flow regardless of pressure", "High speed operation", "Simple design"],
                "correct_answer": "Constant flow regardless of pressure"
            },
            {
                "question": "The impeller is a key component in centrifugal pumps.",
                "type": "true_false",
                "correct_answer": "true"
            },
            {
                "question": "Name one type of positive displacement pump.",
                "type": "short_answer",
                "correct_answer": "Gear pump"
            }
        ]
    })
    
    print("Course created successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(create_course())
