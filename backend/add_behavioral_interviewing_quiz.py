import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Behavioral interviewing is based on the premise that:",
        "options": ["Candidates will always tell the truth in interviews", "Past behavior is the best predictor of future performance", "Technical skills are more important than soft skills", "All candidates perform equally under pressure"],
        "correct_answer": "Past behavior is the best predictor of future performance"
    },
    {
        "question": "The STAR technique in behavioral interviewing stands for:",
        "options": ["Skills, Tasks, Actions, Results", "Situation, Task, Action, Result", "Strategy, Timing, Assessment, Review", "Scenario, Target, Approach, Rating"],
        "correct_answer": "Situation, Task, Action, Result"
    },
    {
        "question": "Which of the following is a behavioral interview question?",
        "options": ["Where do you see yourself in five years?", "What are your greatest strengths?", "Tell me about a time you resolved a conflict with a colleague.", "Why do you want to work here?"],
        "correct_answer": "Tell me about a time you resolved a conflict with a colleague."
    },
    {
        "question": "The primary advantage of behavioral interviewing over traditional interviewing is:",
        "options": ["It is faster to conduct", "It provides concrete evidence of how a candidate has performed in real situations", "It requires no preparation from the interviewer", "It focuses on hypothetical future scenarios"],
        "correct_answer": "It provides concrete evidence of how a candidate has performed in real situations"
    },
    {
        "question": "Before conducting a behavioral interview, an employer should:",
        "options": ["Improvise questions based on the candidate's CV", "Identify the key competencies required for the role and prepare structured questions around them", "Ask only general personality questions", "Focus exclusively on technical qualifications"],
        "correct_answer": "Identify the key competencies required for the role and prepare structured questions around them"
    },
    {
        "question": "When a candidate gives a vague answer in a behavioral interview, the interviewer should:",
        "options": ["Accept the answer and move on", "Use probing follow-up questions to draw out specific details", "End the interview immediately", "Suggest the correct answer to the candidate"],
        "correct_answer": "Use probing follow-up questions to draw out specific details"
    },
    {
        "question": "Which competency would a behavioral question about 'a time you met a tight deadline' be designed to assess?",
        "options": ["Creativity", "Time management and resilience under pressure", "Technical expertise", "Financial acumen"],
        "correct_answer": "Time management and resilience under pressure"
    },
    {
        "question": "A structured behavioral interview ensures:",
        "options": ["All candidates are asked different questions based on their CV", "All candidates are assessed against the same competencies using consistent questions, improving fairness and reliability", "The interviewer can change questions freely during the interview", "Only senior managers conduct the interviews"],
        "correct_answer": "All candidates are assessed against the same competencies using consistent questions, improving fairness and reliability"
    },
    {
        "question": "Which of the following is an example of a probing follow-up question in a behavioral interview?",
        "options": ["Do you enjoy working in teams?", "What specifically did you do to resolve the situation?", "Are you a good communicator?", "Would you describe yourself as a leader?"],
        "correct_answer": "What specifically did you do to resolve the situation?"
    },
    {
        "question": "Scoring rubrics in behavioral interviews are used to:",
        "options": ["Rank candidates by appearance", "Provide a consistent framework for evaluating and comparing candidate responses objectively", "Speed up the interview process", "Eliminate the need for multiple interviewers"],
        "correct_answer": "Provide a consistent framework for evaluating and comparing candidate responses objectively"
    },
    {
        "question": "Which of the following should an interviewer avoid during a behavioral interview?",
        "options": ["Taking notes on candidate responses", "Asking leading questions that suggest the desired answer", "Using the STAR framework to evaluate answers", "Probing for specific examples"],
        "correct_answer": "Asking leading questions that suggest the desired answer"
    },
    {
        "question": "Panel behavioral interviews involve:",
        "options": ["One interviewer and multiple candidates simultaneously", "Multiple interviewers assessing the same candidate, reducing individual bias", "Only HR staff conducting the interview", "Candidates interviewing each other"],
        "correct_answer": "Multiple interviewers assessing the same candidate, reducing individual bias"
    },
    {
        "question": "When evaluating a STAR response, the most important element to assess is:",
        "options": ["The length of the answer", "The Result — what the candidate achieved and the impact of their actions", "The Situation — how complex the context was", "The Task — how difficult the assignment was"],
        "correct_answer": "The Result — what the candidate achieved and the impact of their actions"
    },
    {
        "question": "Behavioral interviewing helps reduce hiring bias by:",
        "options": ["Allowing interviewers to rely on gut feeling", "Focusing on evidence-based competency assessment rather than subjective impressions", "Eliminating all interview questions", "Allowing candidates to choose their own questions"],
        "correct_answer": "Focusing on evidence-based competency assessment rather than subjective impressions"
    },
    {
        "question": "Which of the following best describes a competency-based interview?",
        "options": ["An interview focused only on technical skills testing", "An interview structured around assessing specific behavioural competencies required for the role", "An informal conversation about the candidate's career history", "An interview conducted entirely online"],
        "correct_answer": "An interview structured around assessing specific behavioural competencies required for the role"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "behavioral interviewing", "$options": "i"}})
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
        "title": "Behavioral Interviewing Techniques for Employers - Final Assessment",
        "description": "Test your knowledge of behavioral interviewing, the STAR technique, competency assessment and structured interview design. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
