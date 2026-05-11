import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Strategic HR management involves:",
        "options": ["Managing only the administrative functions of HR", "Aligning HR practices and people strategies with the organisation's overall business strategy to drive performance", "Focusing exclusively on recruitment and payroll", "Managing HR compliance and legal requirements only"],
        "correct_answer": "Aligning HR practices and people strategies with the organisation's overall business strategy to drive performance"
    },
    {
        "question": "The HR Business Partner (HRBP) model positions HR professionals as:",
        "options": ["Administrative support for line managers", "Strategic partners who work closely with business leaders to align people strategies with business objectives", "Compliance officers who enforce HR policies", "Recruitment specialists only"],
        "correct_answer": "Strategic partners who work closely with business leaders to align people strategies with business objectives"
    },
    {
        "question": "A strategic workforce plan addresses:",
        "options": ["Only current staffing levels", "The future talent needs of the organisation based on business strategy, including skills gaps, succession and workforce composition", "Only the annual recruitment plan", "The HR department's internal staffing needs"],
        "correct_answer": "The future talent needs of the organisation based on business strategy, including skills gaps, succession and workforce composition"
    },
    {
        "question": "Employer branding in strategic HR refers to:",
        "options": ["The company's product marketing strategy", "The organisation's reputation as an employer and the value proposition it offers to current and prospective employees", "The HR department's internal communications", "The company's corporate social responsibility programme"],
        "correct_answer": "The organisation's reputation as an employer and the value proposition it offers to current and prospective employees"
    },
    {
        "question": "Change management is a strategic HR competency because:",
        "options": ["HR is responsible for all organisational changes", "HR plays a critical role in preparing, supporting and guiding employees through organisational change to minimise disruption and resistance", "Change management is only relevant during mergers and acquisitions", "HR only communicates changes decided by senior leadership"],
        "correct_answer": "HR plays a critical role in preparing, supporting and guiding employees through organisational change to minimise disruption and resistance"
    },
    {
        "question": "Organisational design in strategic HR involves:",
        "options": ["Designing the company's office layout", "Structuring roles, reporting relationships and processes to enable the organisation to execute its strategy effectively", "Creating the company's brand identity", "Designing the HR department's internal processes only"],
        "correct_answer": "Structuring roles, reporting relationships and processes to enable the organisation to execute its strategy effectively"
    },
    {
        "question": "Total rewards strategy in strategic HR encompasses:",
        "options": ["Only base salary and annual bonuses", "All financial and non-financial rewards including salary, benefits, recognition, career development and work environment", "Only statutory benefits required by law", "Only performance-related pay"],
        "correct_answer": "All financial and non-financial rewards including salary, benefits, recognition, career development and work environment"
    },
    {
        "question": "HR analytics in strategic HR is used to:",
        "options": ["Replace human judgement in all HR decisions", "Use data and evidence to inform strategic people decisions, measure HR effectiveness and predict future workforce trends", "Track only employee attendance data", "Automate all HR administrative processes"],
        "correct_answer": "Use data and evidence to inform strategic people decisions, measure HR effectiveness and predict future workforce trends"
    },
    {
        "question": "Succession planning as a strategic HR activity ensures:",
        "options": ["All employees are promoted on a fixed schedule", "Critical roles have identified and developed internal successors, reducing the risk of leadership gaps", "Only external candidates are considered for senior roles", "All employees receive the same development opportunities"],
        "correct_answer": "Critical roles have identified and developed internal successors, reducing the risk of leadership gaps"
    },
    {
        "question": "A learning organisation in strategic HR is one that:",
        "options": ["Only invests in formal classroom training", "Continuously builds its capacity to learn, adapt and innovate through individual and collective learning at all levels", "Limits learning to new employees during onboarding", "Focuses learning investment only on high-potential employees"],
        "correct_answer": "Continuously builds its capacity to learn, adapt and innovate through individual and collective learning at all levels"
    },
    {
        "question": "Employee value proposition (EVP) in strategic HR defines:",
        "options": ["The financial value of each employee to the organisation", "The unique set of benefits and experiences an organisation offers employees in exchange for their skills, capabilities and commitment", "The company's product value to customers", "The HR department's service offering to line managers"],
        "correct_answer": "The unique set of benefits and experiences an organisation offers employees in exchange for their skills, capabilities and commitment"
    },
    {
        "question": "Diversity and inclusion as a strategic HR priority contributes to:",
        "options": ["Increased administrative complexity only", "Greater innovation, improved decision-making, stronger talent attraction and a more engaged workforce", "Reduced need for performance management", "Simplified recruitment processes"],
        "correct_answer": "Greater innovation, improved decision-making, stronger talent attraction and a more engaged workforce"
    },
    {
        "question": "The strategic role of HR in mergers and acquisitions includes:",
        "options": ["Only managing the legal documentation", "Cultural integration, talent retention, organisational design and change management to ensure the merger delivers its intended value", "Only processing redundancies", "Managing only the financial due diligence"],
        "correct_answer": "Cultural integration, talent retention, organisational design and change management to ensure the merger delivers its intended value"
    },
    {
        "question": "HR metrics that demonstrate strategic value include:",
        "options": ["Only the number of HR staff per employee", "Revenue per employee, time-to-fill, employee engagement scores, turnover cost and training ROI", "Only compliance audit results", "Only the HR department's budget variance"],
        "correct_answer": "Revenue per employee, time-to-fill, employee engagement scores, turnover cost and training ROI"
    },
    {
        "question": "The ultimate goal of strategic HR management is to:",
        "options": ["Reduce the HR department's headcount", "Build organisational capability and a high-performance culture that enables the business to achieve its strategic objectives sustainably", "Eliminate all HR administrative tasks through automation", "Focus exclusively on cost reduction in people management"],
        "correct_answer": "Build organisational capability and a high-performance culture that enables the business to achieve its strategic objectives sustainably"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "diploma in strategic hr", "$options": "i"}})
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
        "title": "Diploma in Strategic HR - Final Assessment",
        "description": "Test your knowledge of strategic HR management, workforce planning, HR analytics, change management and organisational design. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
