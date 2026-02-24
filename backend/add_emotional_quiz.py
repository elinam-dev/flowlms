import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": {"$regex": "Emotional resilience at work", "$options": "i"}})
    
    questions = [
        {"question": "Resilience is the ability to bounce back from adversity.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is the primary benefit of emotional resilience?", "type": "multiple_choice", "options": ["Avoiding all stress", "Coping with stress and challenges effectively", "Never experiencing setbacks", "Being emotionless"], "correct_answer": "Coping with stress and challenges effectively"},
        {"question": "Resilience can be developed and strengthened over time.", "type": "true_false", "correct_answer": "true"},
        {"question": "Which of these is a key component of resilience?", "type": "multiple_choice", "options": ["Perfectionism", "Flexibility and adaptability", "Avoiding change", "Isolation"], "correct_answer": "Flexibility and adaptability"},
        {"question": "Stress always has negative effects on performance.", "type": "true_false", "correct_answer": "false"},
        {"question": "What does VUCA stand for?", "type": "multiple_choice", "options": ["Very Unusual Challenging Attitude", "Volatility, Uncertainty, Complexity, Ambiguity", "Vision, Unity, Clarity, Action", "Value, Understanding, Commitment, Achievement"], "correct_answer": "Volatility, Uncertainty, Complexity, Ambiguity"},
        {"question": "Mindfulness practices can enhance resilience.", "type": "true_false", "correct_answer": "true"},
        {"question": "Which emotion is part of the change curve?", "type": "multiple_choice", "options": ["All emotions listed", "Denial", "Anger", "Acceptance"], "correct_answer": "All emotions listed"},
        {"question": "Social connections are important for building resilience.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is anti-fragility?", "type": "multiple_choice", "options": ["Being weak", "Getting stronger from adversity", "Avoiding challenges", "Being inflexible"], "correct_answer": "Getting stronger from adversity"},
        {"question": "Optimism plays a role in resilience.", "type": "true_false", "correct_answer": "true"},
        {"question": "Which is an action strategy for resilience?", "type": "multiple_choice", "options": ["Feel in control", "Avoid all problems", "Never ask for help", "Ignore emotions"], "correct_answer": "Feel in control"},
        {"question": "Too much resilience can be problematic.", "type": "true_false", "correct_answer": "true"},
        {"question": "What helps in personal transition through change?", "type": "multiple_choice", "options": ["Denying the change", "Understanding emotions", "Avoiding others", "Staying rigid"], "correct_answer": "Understanding emotions"},
        {"question": "Energy levels affect resilience capacity.", "type": "true_false", "correct_answer": "true"},
        {"question": "Which is NOT a benefit of resilience?", "type": "multiple_choice", "options": ["Better stress management", "Improved adaptability", "Avoiding all challenges", "Enhanced wellbeing"], "correct_answer": "Avoiding all challenges"},
        {"question": "Coaching can help develop resilience.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is important for organizational resilience?", "type": "multiple_choice", "options": ["Rigid structures", "Adaptability and flexibility", "Avoiding change", "Individual work only"], "correct_answer": "Adaptability and flexibility"},
        {"question": "Personal vision helps build resilience.", "type": "true_false", "correct_answer": "true"},
        {"question": "Which best describes resilient people?", "type": "multiple_choice", "options": ["They never fail", "They adapt and grow from setbacks", "They avoid all risks", "They work alone"], "correct_answer": "They adapt and grow from setbacks"}
    ]
    
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "course_id": course["id"],
        "title": "Emotional Resilience Final Assessment",
        "passing_score": 70,
        "questions": questions
    })
    
    print("Added final quiz with 20 questions")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
