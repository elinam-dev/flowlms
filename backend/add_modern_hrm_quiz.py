import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "The recruitment process begins with:",
        "options": ["Conducting interviews with candidates", "Identifying a vacancy and defining the role requirements through a job analysis", "Sending offer letters to selected candidates", "Conducting background checks on applicants"],
        "correct_answer": "Identifying a vacancy and defining the role requirements through a job analysis"
    },
    {
        "question": "A job description in recruitment serves to:",
        "options": ["Set the candidate's salary expectations", "Define the duties, responsibilities, reporting relationships and working conditions of the role", "Replace the need for a person specification", "Describe the company's history and culture only"],
        "correct_answer": "Define the duties, responsibilities, reporting relationships and working conditions of the role"
    },
    {
        "question": "A person specification outlines:",
        "options": ["The physical layout of the work environment", "The knowledge, skills, experience, qualifications and personal attributes required of the ideal candidate", "The salary and benefits package for the role", "The company's organisational structure"],
        "correct_answer": "The knowledge, skills, experience, qualifications and personal attributes required of the ideal candidate"
    },
    {
        "question": "The Employee Value Proposition (EVP) in recruitment refers to:",
        "options": ["The financial value of each employee to the business", "The unique set of benefits and experiences the organisation offers to attract and retain talent", "The employee's contribution to company profits", "The value of the employee's skills in the job market"],
        "correct_answer": "The unique set of benefits and experiences the organisation offers to attract and retain talent"
    },
    {
        "question": "Internal recruitment involves:",
        "options": ["Hiring candidates from external job boards only", "Filling vacancies by promoting or transferring existing employees within the organisation", "Using recruitment agencies to source candidates", "Advertising roles on social media platforms"],
        "correct_answer": "Filling vacancies by promoting or transferring existing employees within the organisation"
    },
    {
        "question": "Recruitment metrics help organisations to:",
        "options": ["Replace the need for HR involvement in hiring", "Measure the effectiveness and efficiency of the recruitment process using data such as time-to-fill, cost-per-hire and quality of hire", "Automate all hiring decisions", "Eliminate the need for structured interviews"],
        "correct_answer": "Measure the effectiveness and efficiency of the recruitment process using data such as time-to-fill, cost-per-hire and quality of hire"
    },
    {
        "question": "A structured selection process ensures:",
        "options": ["All candidates are asked different questions based on their CV", "All candidates are assessed consistently against the same criteria, improving fairness and the quality of hiring decisions", "Only the hiring manager makes the final decision without HR involvement", "The process is completed as quickly as possible"],
        "correct_answer": "All candidates are assessed consistently against the same criteria, improving fairness and the quality of hiring decisions"
    },
    {
        "question": "Assessment centres in selection are used to:",
        "options": ["Conduct only psychometric testing", "Evaluate candidates through multiple exercises such as role plays, group discussions and presentations to assess competencies in action", "Replace the need for interviews", "Assess only technical skills"],
        "correct_answer": "Evaluate candidates through multiple exercises such as role plays, group discussions and presentations to assess competencies in action"
    },
    {
        "question": "Situational response questions in interviews ask candidates to:",
        "options": ["Describe their past work experience in detail", "Explain how they would handle a hypothetical work scenario, assessing their judgement and approach", "List their technical qualifications", "Describe their ideal working environment"],
        "correct_answer": "Explain how they would handle a hypothetical work scenario, assessing their judgement and approach"
    },
    {
        "question": "Role plays as an assessment tool in selection are effective because:",
        "options": ["They are the cheapest assessment method", "They allow assessors to observe how candidates actually behave in realistic work situations rather than relying on self-reported answers", "They replace the need for reference checks", "They are only suitable for senior management roles"],
        "correct_answer": "They allow assessors to observe how candidates actually behave in realistic work situations rather than relying on self-reported answers"
    },
    {
        "question": "An assessment form in the selection process is used to:",
        "options": ["Record the candidate's personal details only", "Document evaluators' ratings and observations against defined criteria to support objective, evidence-based hiring decisions", "Set the candidate's starting salary", "Replace the interview debrief discussion"],
        "correct_answer": "Document evaluators' ratings and observations against defined criteria to support objective, evidence-based hiring decisions"
    },
    {
        "question": "Onboarding and induction following selection are important because:",
        "options": ["They are only required for graduate hires", "They help new employees integrate quickly, understand their role and become productive, reducing early turnover", "They replace the need for a probation period", "They are only relevant for large organisations"],
        "correct_answer": "They help new employees integrate quickly, understand their role and become productive, reducing early turnover"
    },
    {
        "question": "Diversity in recruitment is promoted by:",
        "options": ["Advertising roles only through one channel", "Using inclusive job descriptions, diverse sourcing channels and structured assessments to attract and fairly evaluate candidates from all backgrounds", "Hiring only candidates who match the existing team profile", "Relying solely on employee referrals"],
        "correct_answer": "Using inclusive job descriptions, diverse sourcing channels and structured assessments to attract and fairly evaluate candidates from all backgrounds"
    },
    {
        "question": "The role outcomes approach to recruitment focuses on:",
        "options": ["Listing all tasks the employee will perform", "Defining what the employee needs to achieve in the role rather than just what they will do, attracting results-oriented candidates", "Setting the employee's KPIs before they join", "Replacing the job description with a salary range"],
        "correct_answer": "Defining what the employee needs to achieve in the role rather than just what they will do, attracting results-oriented candidates"
    },
    {
        "question": "Modern recruitment channels include:",
        "options": ["Only newspaper advertisements", "LinkedIn, job boards, social media, employee referrals, recruitment agencies and direct sourcing", "Only internal job postings", "Only university campus recruitment"],
        "correct_answer": "LinkedIn, job boards, social media, employee referrals, recruitment agencies and direct sourcing"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "recruitment and selection", "$options": "i"}})
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
        "title": "Modern HRM: Recruitment and Selection Process - Final Assessment",
        "description": "Test your knowledge of recruitment strategy, job analysis, selection methods and assessment tools. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
