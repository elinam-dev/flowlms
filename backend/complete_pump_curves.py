import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def complete_course():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Find the course and module
    course = await db.courses.find_one({"code": "ENG-PUMP-002"})
    if not course:
        print("Course not found!")
        return
    
    course_id = str(course["_id"])
    module = await db.modules.find_one({"course_id": course_id})
    module_id = str(module["_id"])
    
    print(f"Found course: {course_id}, module: {module_id}")
    
    # Create 38 lessons
    for i in range(1, 39):
        lesson = {
            "_id": ObjectId(),
            "module_id": module_id,
            "title": f"Slide {i}",
            "content": f'<div style="text-align: center;"><img src="http://127.0.0.1:8000/api/uploads/images/PUMP CURVES, SELECTION & MATERIAL CHOOSING_{i:02d}.png" alt="Slide {i}" style="max-width: 100%; height: auto;" /></div>',
            "order": i,
            "duration": 2,
            "created_at": datetime.utcnow()
        }
        await db.lessons.insert_one(lesson)
    
    print("Created 38 lessons")
    
    # Create quiz
    quiz = {
        "course_id": course_id,
        "title": "Pump Curves & Selection Assessment",
        "passing_score": 70,
        "questions": [
            {
                "question": "What is the primary purpose of a pump performance curve?",
                "type": "multiple_choice",
                "options": ["To show pump efficiency", "To display flow rate vs head relationship", "To indicate power consumption", "To measure temperature"],
                "correct_answer": "To display flow rate vs head relationship"
            },
            {
                "question": "Material selection for pump components depends on the fluid being pumped.",
                "type": "true_false",
                "correct_answer": "true"
            },
            {
                "question": "What factors should be considered when selecting a pump?",
                "type": "multiple_choice",
                "options": ["Flow rate and head only", "Flow rate, head, fluid properties, and efficiency", "Only the cost", "Only the brand"],
                "correct_answer": "Flow rate, head, fluid properties, and efficiency"
            },
            {
                "question": "The Best Efficiency Point (BEP) is where the pump operates most efficiently.",
                "type": "true_false",
                "correct_answer": "true"
            },
            {
                "question": "What does NPSH stand for in pump terminology?",
                "type": "short_answer",
                "correct_answer": "Net Positive Suction Head"
            }
        ],
        "created_at": datetime.utcnow()
    }
    
    await db.quizzes.insert_one(quiz)
    print("Created quiz")
    
    client.close()
    print("\n✅ Course completed successfully!")

if __name__ == "__main__":
    asyncio.run(complete_course())
