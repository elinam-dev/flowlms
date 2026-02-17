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
        "title": "Valve Presentation",
        "code": "ENG-VALVE-001",
        "description": "Comprehensive training on valve types, applications, and selection criteria.",
        "category": "Engineering",
        "level": "Intermediate",
        "duration": 50,
        "is_compulsory": False,
        "is_published": True,
        "thumbnail": "http://127.0.0.1:8000/api/uploads/images/Valve Presentation_01.png"
    })
    
    # Create module
    await db.modules.insert_one({
        "id": module_id,
        "course_id": course_id,
        "title": "Valve Presentation",
        "description": "Complete presentation on valves",
        "order": 1
    })
    
    # Create 18 lessons
    for i in range(1, 19):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": f"Slide {i}",
            "content_type": "text",
            "content": f'<div style="text-align: center;"><img src="http://127.0.0.1:8000/api/uploads/images/Valve Presentation_{i:02d}.png" alt="Slide {i}" style="max-width: 100%; height: auto;" /></div>',
            "duration_minutes": 2,
            "order": i - 1
        })
    
    # Create quiz
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "course_id": course_id,
        "title": "Valve Knowledge Assessment",
        "passing_score": 70,
        "questions": [
            {
                "question": "What is the primary function of a valve?",
                "type": "multiple_choice",
                "options": ["To increase pressure", "To control flow of fluids", "To measure temperature", "To filter liquids"],
                "correct_answer": "To control flow of fluids"
            },
            {
                "question": "Gate valves are best suited for on/off service rather than throttling.",
                "type": "true_false",
                "correct_answer": "true"
            },
            {
                "question": "Which valve type is commonly used for throttling applications?",
                "type": "multiple_choice",
                "options": ["Gate valve", "Globe valve", "Check valve", "Plug valve"],
                "correct_answer": "Globe valve"
            },
            {
                "question": "Check valves prevent backflow in piping systems.",
                "type": "true_false",
                "correct_answer": "true"
            },
            {
                "question": "Name one type of valve used for isolation purposes.",
                "type": "short_answer",
                "correct_answer": "Gate valve"
            }
        ]
    })
    
    print("Course created successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(create_course())
