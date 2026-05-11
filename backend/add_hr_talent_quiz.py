import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Talent management is defined as:",
        "options": ["Managing only high-performing employees", "The strategic process of attracting, developing, retaining and deploying talented employees to meet current and future organisational needs", "The administration of employee benefits and payroll", "Managing the recruitment process only"],
        "correct_answer": "The strategic process of attracting, developing, retaining and deploying talented employees to meet current and future organisational needs"
    },
    {
        "question": "Workforce development focuses on:",
        "options": ["Reducing the number of employees in the organisation", "Building the skills, knowledge and capabilities of employees to improve performance and prepare for future roles", "Managing employee attendance and punctuality", "Setting the annual salary review budget"],
        "correct_answer": "Building the skills, knowledge and capabilities of employees to improve performance and prepare for future roles"
    },
    {
        "question": "Effective interviewing techniques in talent management help organisations to:",
        "options": ["Speed up the hiring process at the expense of quality", "Select candidates whose competencies, values and potential align with the role and organisational culture", "Reduce the number of interview rounds", "Eliminate the need for reference checks"],
        "correct_answer": "Select candidates whose competencies, values and potential align with the role and organisational culture"
    },
    {
        "question": "Orientation for new employees is designed to:",
        "options": ["Assess whether the new hire was the right choice", "Help new employees understand the organisation, their role and the people they will work with, accelerating their integration", "Complete all compliance paperwork on day one", "Replace the need for ongoing onboarding support"],
        "correct_answer": "Help new employees understand the organisation, their role and the people they will work with, accelerating their integration"
    },
    {
        "question": "Employee retention strategies are important because:",
        "options": ["High turnover has no impact on organisational performance", "Retaining talented employees reduces recruitment costs, preserves institutional knowledge and maintains team stability", "All employees should be replaced regularly to bring in fresh ideas", "Retention is only relevant for senior leadership roles"],
        "correct_answer": "Retaining talented employees reduces recruitment costs, preserves institutional knowledge and maintains team stability"
    },
    {
        "question": "Workplace health and safety is a talent management concern because:",
        "options": ["It only affects the facilities management team", "A safe and healthy work environment supports employee wellbeing, reduces absenteeism and demonstrates the organisation's duty of care", "It is only relevant in manufacturing environments", "It has no impact on employee engagement or retention"],
        "correct_answer": "A safe and healthy work environment supports employee wellbeing, reduces absenteeism and demonstrates the organisation's duty of care"
    },
    {
        "question": "Bullying and harassment in the workplace must be addressed by HR because:",
        "options": ["It only affects the individuals directly involved", "It creates a toxic work environment, reduces productivity, increases turnover and exposes the organisation to legal liability", "It is a minor issue that resolves itself over time", "It only requires informal resolution without documentation"],
        "correct_answer": "It creates a toxic work environment, reduces productivity, increases turnover and exposes the organisation to legal liability"
    },
    {
        "question": "Promoting workplace wellness as part of talent management involves:",
        "options": ["Only providing gym memberships to employees", "Implementing programmes that support physical, mental and emotional wellbeing to improve engagement, productivity and retention", "Reducing employee workloads permanently", "Only addressing wellness issues after they become serious"],
        "correct_answer": "Implementing programmes that support physical, mental and emotional wellbeing to improve engagement, productivity and retention"
    },
    {
        "question": "Providing effective feedback to employees is important because:",
        "options": ["It replaces the need for formal performance reviews", "Regular, constructive feedback helps employees understand their performance, develop their skills and stay engaged", "Feedback should only be given when performance is poor", "Positive feedback is the only type that improves performance"],
        "correct_answer": "Regular, constructive feedback helps employees understand their performance, develop their skills and stay engaged"
    },
    {
        "question": "Disciplining an employee fairly requires:",
        "options": ["Immediate dismissal for any performance issue", "Following a consistent, documented process that gives the employee the opportunity to understand the issue and improve", "Only verbal warnings with no written documentation", "Involving all team members in the disciplinary discussion"],
        "correct_answer": "Following a consistent, documented process that gives the employee the opportunity to understand the issue and improve"
    },
    {
        "question": "Terminating an employee should be done:",
        "options": ["Without any prior warning or process", "Only after a fair process has been followed, the employee has been given the opportunity to improve and all documentation is in order", "Immediately upon any performance concern", "Without informing HR or documenting the reasons"],
        "correct_answer": "Only after a fair process has been followed, the employee has been given the opportunity to improve and all documentation is in order"
    },
    {
        "question": "Following up with new employees after their first few weeks helps to:",
        "options": ["Assess whether they should be retained beyond probation only", "Identify challenges early, provide support and reinforce their sense of belonging and commitment to the organisation", "Reduce the manager's involvement in onboarding", "Complete the remaining compliance training"],
        "correct_answer": "Identify challenges early, provide support and reinforce their sense of belonging and commitment to the organisation"
    },
    {
        "question": "A talent pipeline in workforce development refers to:",
        "options": ["A list of all current job vacancies", "A pool of identified and developed internal candidates ready to fill critical roles as they become available", "The company's recruitment advertising channels", "The HR department's succession plan for itself"],
        "correct_answer": "A pool of identified and developed internal candidates ready to fill critical roles as they become available"
    },
    {
        "question": "The HR concept today recognises that people are:",
        "options": ["A cost to be minimised", "The organisation's most valuable asset and a source of sustainable competitive advantage", "Interchangeable resources with no unique value", "Only relevant to the HR department's planning"],
        "correct_answer": "The organisation's most valuable asset and a source of sustainable competitive advantage"
    },
    {
        "question": "Workforce development contributes to organisational success by:",
        "options": ["Reducing the need for external recruitment permanently", "Building a capable, engaged and adaptable workforce that can meet current demands and future strategic challenges", "Eliminating the need for performance management", "Focusing only on technical skills training"],
        "correct_answer": "Building a capable, engaged and adaptable workforce that can meet current demands and future strategic challenges"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "talent management and workforce", "$options": "i"}})
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
        "title": "HR: Talent Management and Workforce Development - Final Assessment",
        "description": "Test your knowledge of talent management, workforce development, retention, wellness and employee lifecycle management. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
