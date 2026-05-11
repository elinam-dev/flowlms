import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Employee management involves:",
        "options": ["Only managing employee payroll and benefits", "Overseeing the performance, development, engagement and wellbeing of employees to achieve organisational goals", "Managing only underperforming employees", "Administering HR policies and procedures exclusively"],
        "correct_answer": "Overseeing the performance, development, engagement and wellbeing of employees to achieve organisational goals"
    },
    {
        "question": "A Training Needs Analysis (TNA) is conducted to:",
        "options": ["Determine the training budget for the year", "Identify the gap between current employee skills and the skills required to meet business objectives", "Select the training provider for the year", "Assess employee satisfaction with existing training"],
        "correct_answer": "Identify the gap between current employee skills and the skills required to meet business objectives"
    },
    {
        "question": "On-the-job training (OJT) is effective because:",
        "options": ["It is the cheapest form of training", "It allows employees to learn in the actual work environment, applying skills immediately in real situations", "It requires no manager involvement", "It is only suitable for new employees"],
        "correct_answer": "It allows employees to learn in the actual work environment, applying skills immediately in real situations"
    },
    {
        "question": "The Kirkpatrick Model for evaluating training effectiveness measures:",
        "options": ["Only the cost of training programmes", "Four levels: Reaction, Learning, Behaviour and Results", "Only employee satisfaction with the training", "Only the financial return on training investment"],
        "correct_answer": "Four levels: Reaction, Learning, Behaviour and Results"
    },
    {
        "question": "A Personal Development Plan (PDP) is used to:",
        "options": ["Document an employee's disciplinary history", "Set out an individual's learning and development goals, actions and timelines to support their growth and career progression", "Replace the annual performance review", "Manage the employee's salary progression"],
        "correct_answer": "Set out an individual's learning and development goals, actions and timelines to support their growth and career progression"
    },
    {
        "question": "Coaching as a development tool in employee management involves:",
        "options": ["Telling employees exactly what to do in every situation", "A structured, one-to-one process that helps employees develop their thinking, skills and performance through questioning and reflection", "Only addressing performance problems", "Providing technical training on specific job tasks"],
        "correct_answer": "A structured, one-to-one process that helps employees develop their thinking, skills and performance through questioning and reflection"
    },
    {
        "question": "Mentoring in the workplace differs from coaching in that it:",
        "options": ["Is always more formal than coaching", "Involves a more experienced person sharing knowledge, experience and guidance to support a less experienced employee's development", "Focuses only on short-term performance improvement", "Is only used for graduate trainees"],
        "correct_answer": "Involves a more experienced person sharing knowledge, experience and guidance to support a less experienced employee's development"
    },
    {
        "question": "Employee engagement is best described as:",
        "options": ["Employee attendance and punctuality", "The emotional commitment an employee has to the organisation and its goals, driving discretionary effort and performance", "Employee satisfaction with their salary", "The number of years an employee has worked for the organisation"],
        "correct_answer": "The emotional commitment an employee has to the organisation and its goals, driving discretionary effort and performance"
    },
    {
        "question": "Managing a diverse team effectively requires:",
        "options": ["Treating all team members identically regardless of their needs", "Recognising individual differences, adapting management style and creating an inclusive environment where everyone can contribute", "Focusing only on team members with the highest performance ratings", "Avoiding any discussion of differences within the team"],
        "correct_answer": "Recognising individual differences, adapting management style and creating an inclusive environment where everyone can contribute"
    },
    {
        "question": "Blended learning in employee training combines:",
        "options": ["Only classroom and online training", "Multiple learning methods such as e-learning, classroom sessions, on-the-job practice and coaching to maximise effectiveness", "Only formal and informal learning", "Only internal and external training providers"],
        "correct_answer": "Multiple learning methods such as e-learning, classroom sessions, on-the-job practice and coaching to maximise effectiveness"
    },
    {
        "question": "A learning management system (LMS) is used to:",
        "options": ["Manage employee payroll", "Deliver, track and manage employee training and development activities digitally", "Conduct performance appraisals", "Manage the recruitment process"],
        "correct_answer": "Deliver, track and manage employee training and development activities digitally"
    },
    {
        "question": "Succession planning in employee management ensures:",
        "options": ["All employees are promoted on a fixed schedule", "Key roles have identified and prepared internal successors, reducing the risk of critical talent gaps", "Only external candidates are considered for leadership roles", "All employees receive the same development plan"],
        "correct_answer": "Key roles have identified and prepared internal successors, reducing the risk of critical talent gaps"
    },
    {
        "question": "The 70-20-10 learning model suggests that effective development comes from:",
        "options": ["70% classroom training, 20% e-learning, 10% coaching", "70% on-the-job experience, 20% learning from others and 10% formal training", "70% formal training, 20% mentoring, 10% self-study", "Equal parts formal, informal and social learning"],
        "correct_answer": "70% on-the-job experience, 20% learning from others and 10% formal training"
    },
    {
        "question": "Recognising and rewarding employee contributions is important because:",
        "options": ["It replaces the need for competitive salaries", "Recognition reinforces desired behaviours, boosts morale and increases employee engagement and retention", "It is only relevant for high-performing employees", "It reduces the need for performance management"],
        "correct_answer": "Recognition reinforces desired behaviours, boosts morale and increases employee engagement and retention"
    },
    {
        "question": "Effective employee management ultimately contributes to:",
        "options": ["Reducing the HR department's workload only", "A high-performing, engaged and capable workforce that drives organisational success and competitive advantage", "Eliminating the need for external recruitment", "Reducing all people-related costs"],
        "correct_answer": "A high-performing, engaged and capable workforce that drives organisational success and competitive advantage"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "employee management and training", "$options": "i"}})
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
        "title": "Human Resources: Employee Management and Training - Final Assessment",
        "description": "Test your knowledge of employee management, training needs analysis, learning models, coaching and engagement. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
