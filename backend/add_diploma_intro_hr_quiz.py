import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "aae026b3-567e-4078-9fc3-1fe9cbde2b92"

QUESTIONS = [
    {
        "question": "Human Resource Management (HRM) is primarily concerned with:",
        "options": ["Managing the company's financial assets", "Attracting, developing, motivating and retaining employees to achieve organisational goals", "Managing only the recruitment process", "Administering payroll and benefits exclusively"],
        "correct_answer": "Attracting, developing, motivating and retaining employees to achieve organisational goals"
    },
    {
        "question": "The evolution of HR from personnel management to HRM reflects a shift towards:",
        "options": ["A purely administrative and compliance-focused function", "A strategic, people-centred approach that aligns human capital with business objectives", "Reducing the HR department's involvement in business decisions", "Focusing exclusively on employee welfare"],
        "correct_answer": "A strategic, people-centred approach that aligns human capital with business objectives"
    },
    {
        "question": "Human capital refers to:",
        "options": ["The company's physical assets and equipment", "The collective knowledge, skills, experience and capabilities of an organisation's workforce", "The financial capital invested in the business", "The number of employees in the organisation"],
        "correct_answer": "The collective knowledge, skills, experience and capabilities of an organisation's workforce"
    },
    {
        "question": "The HR function in a modern organisation typically includes:",
        "options": ["Only recruitment and payroll administration", "Recruitment, learning and development, performance management, employee relations, compensation and HR strategy", "Only compliance and legal management", "Only training and development activities"],
        "correct_answer": "Recruitment, learning and development, performance management, employee relations, compensation and HR strategy"
    },
    {
        "question": "Employee relations in HRM involves:",
        "options": ["Managing only disciplinary proceedings", "Building and maintaining positive relationships between the organisation and its employees, including handling grievances and promoting engagement", "Managing only trade union negotiations", "Administering employee benefits only"],
        "correct_answer": "Building and maintaining positive relationships between the organisation and its employees, including handling grievances and promoting engagement"
    },
    {
        "question": "The psychological contract in employment refers to:",
        "options": ["The formal written employment contract", "The unwritten set of mutual expectations and obligations between an employer and employee", "The employee's job description and KPIs", "The company's code of conduct"],
        "correct_answer": "The unwritten set of mutual expectations and obligations between an employer and employee"
    },
    {
        "question": "Job analysis in HRM is used to:",
        "options": ["Analyse the company's financial performance", "Systematically gather information about a job's duties, responsibilities, required skills and working conditions to inform HR decisions", "Assess employee performance against targets", "Determine the company's organisational structure"],
        "correct_answer": "Systematically gather information about a job's duties, responsibilities, required skills and working conditions to inform HR decisions"
    },
    {
        "question": "Compensation and benefits management in HRM aims to:",
        "options": ["Minimise all employee-related costs", "Design and administer fair, competitive and motivating reward packages that attract, retain and engage talent", "Only comply with minimum wage legislation", "Set salaries based solely on seniority"],
        "correct_answer": "Design and administer fair, competitive and motivating reward packages that attract, retain and engage talent"
    },
    {
        "question": "HR compliance in an organisation requires:",
        "options": ["Only following internal company policies", "Ensuring all HR practices comply with relevant employment legislation, regulations and ethical standards", "Only managing health and safety requirements", "Compliance is optional for small organisations"],
        "correct_answer": "Ensuring all HR practices comply with relevant employment legislation, regulations and ethical standards"
    },
    {
        "question": "The concept of 'best fit' in strategic HRM means:",
        "options": ["Hiring only candidates who fit the existing team culture", "Aligning HR practices with the specific context, strategy and culture of the organisation rather than applying universal best practices", "Using only industry-standard HR policies", "Fitting all employees into the same performance management framework"],
        "correct_answer": "Aligning HR practices with the specific context, strategy and culture of the organisation rather than applying universal best practices"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"id": COURSE_ID})
    if not course:
        print("Course not found")
        return
    print(f"Found: {course['title']}")
    module = await db.modules.find_one({"course_id": COURSE_ID})
    existing = await db.quizzes.find_one({"module_id": module["id"]})
    if existing:
        await db.quizzes.delete_one({"module_id": module["id"]})
        print("Removed existing quiz")
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module["id"],
        "course_id": COURSE_ID,
        "title": "Diploma in Introduction to Human Resource Concepts - Final Assessment",
        "description": "Test your knowledge of core HR concepts, human capital, employee relations, compensation and strategic HRM. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
