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
        "title": "Presentation On Pump Spares",
        "code": "ENG-PUMP-004",
        "description": "Comprehensive training on pump spare parts, identification, and maintenance.",
        "category": "Engineering",
        "level": "Intermediate",
        "duration": 70,
        "is_compulsory": False,
        "is_published": True,
        "thumbnail": "http://127.0.0.1:8000/api/uploads/images/presentation_on_pump_spares_01.png"
    })
    
    # Create module
    await db.modules.insert_one({
        "id": module_id,
        "course_id": course_id,
        "title": "Pump Spares Presentation",
        "description": "Complete presentation on pump spare parts",
        "order": 1
    })
    
    # Create 29 lessons
    for i in range(1, 30):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": f"Slide {i}",
            "content_type": "text",
            "content": f'<div style="text-align: center;"><img src="http://127.0.0.1:8000/api/uploads/images/presentation_on_pump_spares_{i:02d}.png" alt="Slide {i}" style="max-width: 100%; height: auto;" /></div>',
            "duration_minutes": 2,
            "order": i - 1
        })
    
    # Create quiz
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "course_id": course_id,
        "title": "Pump Spares Assessment",
        "passing_score": 70,
        "questions": [
            {
                "question": "What is the purpose of pump spare parts inventory?",
                "type": "multiple_choice",
                "options": ["To increase costs", "To ensure quick repairs and minimize downtime", "To store old parts", "To display products"],
                "correct_answer": "To ensure quick repairs and minimize downtime"
            },
            {
                "question": "Regular maintenance can extend the life of pump components.",
                "type": "true_false",
                "correct_answer": "true"
            },
            {
                "question": "What should be considered when selecting pump spare parts?",
                "type": "multiple_choice",
                "options": ["Only price", "Compatibility, quality, and availability", "Brand name only", "Color"],
                "correct_answer": "Compatibility, quality, and availability"
            },
            {
                "question": "Genuine spare parts are always recommended over generic alternatives.",
                "type": "true_false",
                "correct_answer": "true"
            },
            {
                "question": "Name one critical spare part for centrifugal pumps.",
                "type": "short_answer",
                "correct_answer": "Impeller"
            }
        ]
    })
    
    print("Course created successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(create_course())
