import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "The 4Cs of employee onboarding stand for:",
        "options": ["Communication, Culture, Compliance, Competency", "Compliance, Clarification, Culture, Connection", "Compliance, Clarity, Coaching, Commitment", "Culture, Competence, Confidence, Contribution"],
        "correct_answer": "Compliance, Clarification, Culture, Connection"
    },
    {
        "question": "The 'Compliance' component of the 4Cs onboarding model covers:",
        "options": ["Teaching the employee company values and norms", "Ensuring the new employee understands legal requirements, company policies and essential rules", "Building relationships with colleagues", "Clarifying role expectations and performance goals"],
        "correct_answer": "Ensuring the new employee understands legal requirements, company policies and essential rules"
    },
    {
        "question": "The 'Clarification' component of the 4Cs ensures that new employees:",
        "options": ["Understand the company's history and founding story", "Have a clear understanding of their job responsibilities, performance expectations and how their role contributes to organisational goals", "Complete all compliance training within the first week", "Are introduced to all colleagues across the organisation"],
        "correct_answer": "Have a clear understanding of their job responsibilities, performance expectations and how their role contributes to organisational goals"
    },
    {
        "question": "The 'Culture' component of the 4Cs onboarding model focuses on:",
        "options": ["Teaching employees technical skills for their role", "Helping new employees understand and integrate into the organisation's values, norms, behaviours and ways of working", "Completing all HR paperwork", "Setting up the employee's IT equipment and access"],
        "correct_answer": "Helping new employees understand and integrate into the organisation's values, norms, behaviours and ways of working"
    },
    {
        "question": "The 'Connection' component of the 4Cs onboarding model is designed to:",
        "options": ["Connect the employee to the company's IT systems", "Build meaningful interpersonal relationships and networks that help the new employee feel welcomed and engaged", "Connect the employee's salary to the payroll system", "Link the employee's goals to the company's financial targets"],
        "correct_answer": "Build meaningful interpersonal relationships and networks that help the new employee feel welcomed and engaged"
    },
    {
        "question": "A welcome email sent before the employee's first day is an example of:",
        "options": ["Compliance onboarding", "Pre-boarding that builds excitement and reduces first-day anxiety", "Culture training", "Performance management"],
        "correct_answer": "Pre-boarding that builds excitement and reduces first-day anxiety"
    },
    {
        "question": "An onboarding checklist is used to:",
        "options": ["Replace the need for a formal induction programme", "Ensure all essential onboarding activities are completed systematically and nothing is overlooked", "Track the new employee's performance during probation", "Assess whether the new hire was the right choice"],
        "correct_answer": "Ensure all essential onboarding activities are completed systematically and nothing is overlooked"
    },
    {
        "question": "The most common reason new employees leave within the first 90 days is:",
        "options": ["The salary was too high", "Poor onboarding — feeling unwelcome, unclear about their role or disconnected from the team and culture", "Too many social events in the first week", "Excessive training requirements"],
        "correct_answer": "Poor onboarding — feeling unwelcome, unclear about their role or disconnected from the team and culture"
    },
    {
        "question": "A case study approach in onboarding training is effective because:",
        "options": ["It reduces the time needed for onboarding", "It provides real-world context that helps new employees apply concepts to practical workplace situations", "It replaces the need for a buddy or mentor", "It eliminates the need for manager involvement"],
        "correct_answer": "It provides real-world context that helps new employees apply concepts to practical workplace situations"
    },
    {
        "question": "Effective onboarding should extend beyond the first day to:",
        "options": ["Only the first week of employment", "At least the first 90 days, with structured support, check-ins and development activities throughout", "Only until the employee completes compliance training", "The end of the probation period with no interim touchpoints"],
        "correct_answer": "At least the first 90 days, with structured support, check-ins and development activities throughout"
    },
    {
        "question": "The role of the line manager in the 4Cs onboarding process is to:",
        "options": ["Delegate all onboarding responsibilities to HR", "Lead the clarification and connection elements by setting clear expectations, providing feedback and building the relationship with the new hire", "Only conduct the formal performance review at end of probation", "Focus only on technical training for the new employee"],
        "correct_answer": "Lead the clarification and connection elements by setting clear expectations, providing feedback and building the relationship with the new hire"
    },
    {
        "question": "Measuring onboarding effectiveness can be done through:",
        "options": ["Only tracking the time taken to complete paperwork", "New hire satisfaction surveys, time-to-productivity metrics, 90-day retention rates and manager feedback", "Only monitoring attendance in the first month", "Counting the number of onboarding activities completed"],
        "correct_answer": "New hire satisfaction surveys, time-to-productivity metrics, 90-day retention rates and manager feedback"
    },
    {
        "question": "Organisational socialisation during onboarding refers to:",
        "options": ["Organising social events for new employees only", "The process by which new employees learn the values, norms, behaviours and knowledge needed to function effectively within the organisation", "Introducing new employees to the company's social media channels", "Scheduling team lunches in the first week"],
        "correct_answer": "The process by which new employees learn the values, norms, behaviours and knowledge needed to function effectively within the organisation"
    },
    {
        "question": "Which of the following best describes a high-quality onboarding programme?",
        "options": ["A one-day induction covering all company policies", "A structured, multi-week programme that addresses compliance, role clarity, cultural integration and relationship building", "An online portal with self-paced modules only", "A single meeting with HR on the first day"],
        "correct_answer": "A structured, multi-week programme that addresses compliance, role clarity, cultural integration and relationship building"
    },
    {
        "question": "The ultimate goal of the 4Cs onboarding model is to:",
        "options": ["Reduce the HR department's administrative workload", "Accelerate new employee integration, engagement and productivity while reducing early turnover", "Complete all legal compliance requirements as quickly as possible", "Assess the new employee's suitability for the role"],
        "correct_answer": "Accelerate new employee integration, engagement and productivity while reducing early turnover"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "ultimate employee onboarding", "$options": "i"}})
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
        "title": "HRM: Ultimate Employee Onboarding Guide with 4Cs - Final Assessment",
        "description": "Test your knowledge of the 4Cs onboarding model, pre-boarding, cultural integration and onboarding best practices. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
