import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Competency mapping in HR is defined as:",
        "options": ["Mapping the physical layout of the HR department", "The process of identifying the key competencies required for each role and assessing employees against those competencies", "Creating an organisational chart", "Mapping employee salaries to market benchmarks"],
        "correct_answer": "The process of identifying the key competencies required for each role and assessing employees against those competencies"
    },
    {
        "question": "A competency is best described as:",
        "options": ["A job title or designation", "A combination of knowledge, skills, behaviours and attitudes that enable effective performance in a role", "An employee's years of experience only", "A technical qualification or degree"],
        "correct_answer": "A combination of knowledge, skills, behaviours and attitudes that enable effective performance in a role"
    },
    {
        "question": "The primary purpose of competency mapping is to:",
        "options": ["Reduce the HR department's workload", "Align human capital capabilities with organisational strategy and identify gaps for development", "Replace performance appraisals entirely", "Automate the recruitment process"],
        "correct_answer": "Align human capital capabilities with organisational strategy and identify gaps for development"
    },
    {
        "question": "Core competencies in an organisation refer to:",
        "options": ["Technical skills specific to one department", "Competencies expected of all employees regardless of role or level, reflecting the organisation's values and culture", "Competencies required only for senior leadership", "Competencies related to financial management"],
        "correct_answer": "Competencies expected of all employees regardless of role or level, reflecting the organisation's values and culture"
    },
    {
        "question": "A competency framework is used to:",
        "options": ["Set employee salaries", "Provide a structured reference that defines the competencies required at each level and role within the organisation", "Track employee attendance", "Manage the company's training budget"],
        "correct_answer": "Provide a structured reference that defines the competencies required at each level and role within the organisation"
    },
    {
        "question": "Behavioural indicators in a competency framework describe:",
        "options": ["The employee's personality type", "Observable actions and behaviours that demonstrate a competency is being applied effectively", "The technical qualifications required for a role", "The salary range for each competency level"],
        "correct_answer": "Observable actions and behaviours that demonstrate a competency is being applied effectively"
    },
    {
        "question": "Competency mapping supports talent management by:",
        "options": ["Eliminating the need for performance reviews", "Identifying high-potential employees, succession candidates and development needs across the organisation", "Reducing the number of employees in the organisation", "Automating all HR processes"],
        "correct_answer": "Identifying high-potential employees, succession candidates and development needs across the organisation"
    },
    {
        "question": "A competency gap analysis identifies:",
        "options": ["The difference between an employee's current salary and market rate", "The difference between the competencies an employee currently demonstrates and those required for their role or future roles", "The number of vacancies in the organisation", "The gap between HR budget and actual spend"],
        "correct_answer": "The difference between the competencies an employee currently demonstrates and those required for their role or future roles"
    },
    {
        "question": "Which method is commonly used to gather data for competency mapping?",
        "options": ["Only reviewing employee CVs", "Structured interviews, behavioural assessments, 360-degree feedback and job analysis", "Reviewing payroll records only", "Conducting exit interviews exclusively"],
        "correct_answer": "Structured interviews, behavioural assessments, 360-degree feedback and job analysis"
    },
    {
        "question": "Functional competencies differ from core competencies in that they:",
        "options": ["Apply to all employees in the organisation", "Are specific to a particular function, department or role", "Are only relevant to senior management", "Are based on academic qualifications only"],
        "correct_answer": "Are specific to a particular function, department or role"
    },
    {
        "question": "Competency mapping contributes to recruitment and selection by:",
        "options": ["Replacing the need for job descriptions", "Providing clear criteria against which candidates can be assessed, improving the quality and consistency of hiring decisions", "Eliminating the need for interviews", "Automating the shortlisting process"],
        "correct_answer": "Providing clear criteria against which candidates can be assessed, improving the quality and consistency of hiring decisions"
    },
    {
        "question": "Leadership competencies typically include:",
        "options": ["Only technical expertise in a specific field", "Strategic thinking, decision-making, people development, communication and change management", "Only financial management skills", "Only operational efficiency skills"],
        "correct_answer": "Strategic thinking, decision-making, people development, communication and change management"
    },
    {
        "question": "Transforming people into human capital through competency mapping means:",
        "options": ["Treating employees as replaceable resources", "Developing and leveraging employees' competencies strategically to create sustainable competitive advantage for the organisation", "Reducing headcount through automation", "Standardising all roles to reduce complexity"],
        "correct_answer": "Developing and leveraging employees' competencies strategically to create sustainable competitive advantage for the organisation"
    },
    {
        "question": "Proficiency levels in a competency framework indicate:",
        "options": ["The employee's salary grade", "The degree to which a competency is demonstrated, ranging from basic awareness to expert mastery", "The number of years an employee has been in a role", "The employee's educational background"],
        "correct_answer": "The degree to which a competency is demonstrated, ranging from basic awareness to expert mastery"
    },
    {
        "question": "Which of the following is a key benefit of implementing competency mapping in an organisation?",
        "options": ["It eliminates the need for training and development", "It creates a common language for performance, development and talent decisions, improving consistency across the organisation", "It reduces the HR team to a purely administrative function", "It replaces the need for organisational strategy"],
        "correct_answer": "It creates a common language for performance, development and talent decisions, improving consistency across the organisation"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "competency mapping", "$options": "i"}})
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
        "title": "Competency Mapping in HR - Final Assessment",
        "description": "Test your knowledge of competency frameworks, gap analysis, behavioural indicators and talent development. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
