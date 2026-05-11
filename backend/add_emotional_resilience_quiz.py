import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Emotional resilience at work is best defined as:",
        "options": ["The ability to avoid all workplace stress", "The capacity to adapt, recover and grow from workplace challenges, setbacks and adversity", "The ability to suppress emotions in professional settings", "A fixed personality trait that cannot be developed"],
        "correct_answer": "The capacity to adapt, recover and grow from workplace challenges, setbacks and adversity"
    },
    {
        "question": "VUCA stands for:",
        "options": ["Vision, Unity, Clarity, Action", "Volatility, Uncertainty, Complexity, Ambiguity", "Value, Understanding, Commitment, Achievement", "Very Unusual Challenging Attitude"],
        "correct_answer": "Volatility, Uncertainty, Complexity, Ambiguity"
    },
    {
        "question": "Which of the following statements about resilience is TRUE?",
        "options": ["Resilience is a fixed trait you are born with", "Resilient people never experience stress or negative emotions", "Resilience can be developed and strengthened through practice and experience", "Resilience means always staying positive regardless of circumstances"],
        "correct_answer": "Resilience can be developed and strengthened through practice and experience"
    },
    {
        "question": "The Change Curve model describes the emotional journey through change as typically including:",
        "options": ["Immediate acceptance followed by action", "Denial, anger, bargaining, depression and acceptance", "Excitement, planning, execution and review", "Confusion, clarity, commitment and completion"],
        "correct_answer": "Denial, anger, bargaining, depression and acceptance"
    },
    {
        "question": "Anti-fragility, as a concept related to resilience, means:",
        "options": ["Being immune to all forms of stress", "Becoming weaker when exposed to adversity", "Growing stronger and improving as a result of exposure to stressors and challenges", "Avoiding all risk and uncertainty"],
        "correct_answer": "Growing stronger and improving as a result of exposure to stressors and challenges"
    },
    {
        "question": "Mindfulness practices support resilience primarily by:",
        "options": ["Eliminating all negative thoughts permanently", "Helping individuals stay present, manage stress responses and regulate emotions more effectively", "Increasing productivity by removing all breaks", "Replacing the need for professional support"],
        "correct_answer": "Helping individuals stay present, manage stress responses and regulate emotions more effectively"
    },
    {
        "question": "Which of the following is a key action strategy for building personal resilience?",
        "options": ["Avoiding all challenging situations", "Maintaining a sense of control, purpose and connection with others", "Working longer hours to prove commitment", "Suppressing emotions to appear professional"],
        "correct_answer": "Maintaining a sense of control, purpose and connection with others"
    },
    {
        "question": "Social connections contribute to resilience because:",
        "options": ["They eliminate the need for personal coping strategies", "Strong relationships provide emotional support, perspective and practical help during difficult times", "They reduce workload automatically", "They prevent any negative events from occurring"],
        "correct_answer": "Strong relationships provide emotional support, perspective and practical help during difficult times"
    },
    {
        "question": "Eustress refers to:",
        "options": ["Chronic negative stress that harms health", "A form of positive stress that motivates and enhances performance", "Stress caused by workplace conflict only", "The complete absence of stress"],
        "correct_answer": "A form of positive stress that motivates and enhances performance"
    },
    {
        "question": "Organisational resilience requires:",
        "options": ["Rigid structures and fixed processes", "Adaptability, flexible systems and a culture that supports learning from setbacks", "Avoiding all change initiatives", "Individual resilience only, with no team component"],
        "correct_answer": "Adaptability, flexible systems and a culture that supports learning from setbacks"
    },
    {
        "question": "Which of the following is NOT a benefit of emotional resilience in the workplace?",
        "options": ["Better stress management", "Improved adaptability to change", "Complete avoidance of all workplace challenges", "Enhanced overall wellbeing"],
        "correct_answer": "Complete avoidance of all workplace challenges"
    },
    {
        "question": "Personal vision supports resilience by:",
        "options": ["Guaranteeing career success", "Providing a sense of direction and purpose that sustains motivation during difficult periods", "Eliminating the need for feedback", "Reducing the importance of relationships at work"],
        "correct_answer": "Providing a sense of direction and purpose that sustains motivation during difficult periods"
    },
    {
        "question": "Energy management is important for resilience because:",
        "options": ["Working without rest builds mental toughness", "Physical, emotional and mental energy levels directly affect our capacity to cope with stress and recover", "Energy is only relevant to physical resilience", "Sleep and recovery are signs of weakness"],
        "correct_answer": "Physical, emotional and mental energy levels directly affect our capacity to cope with stress and recover"
    },
    {
        "question": "Coaching can help develop resilience by:",
        "options": ["Solving all problems on behalf of the individual", "Helping individuals identify strengths, reframe challenges and develop personalised coping strategies", "Replacing the need for self-reflection", "Providing a fixed set of rules to follow in all situations"],
        "correct_answer": "Helping individuals identify strengths, reframe challenges and develop personalised coping strategies"
    },
    {
        "question": "Which statement best describes a resilient person in the workplace?",
        "options": ["They never fail or make mistakes", "They avoid all conflict and difficult conversations", "They adapt, learn from setbacks and maintain effectiveness under pressure", "They always work independently without seeking support"],
        "correct_answer": "They adapt, learn from setbacks and maintain effectiveness under pressure"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "emotional resilience at work", "$options": "i"}})
    if not course:
        print("Course not found")
        return
    print(f"Found: {course['title']}")
    module = await db.modules.find_one({"course_id": course["id"]})
    existing = await db.quizzes.find_one({"module_id": module["id"]})
    if existing:
        await db.quizzes.delete_one({"module_id": module["id"]})
        print("Removed existing quiz")
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module["id"],
        "course_id": course["id"],
        "title": "Emotional Resilience at Work - Final Assessment",
        "description": "Test your understanding of resilience, stress management, the change curve and strategies for building resilience at work. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
