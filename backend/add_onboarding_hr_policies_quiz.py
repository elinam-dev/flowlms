import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "The primary purpose of an employee onboarding programme is to:",
        "options": ["Complete all HR paperwork as quickly as possible", "Help new employees integrate into the organisation, understand their role and become productive contributors", "Assess whether the new hire was the right choice", "Introduce the employee to the payroll system only"],
        "correct_answer": "Help new employees integrate into the organisation, understand their role and become productive contributors"
    },
    {
        "question": "Onboarding preparation before the employee's first day should include:",
        "options": ["Waiting until the employee arrives to set up their workspace", "Preparing the workspace, IT access, welcome materials and notifying the team of the new hire's arrival", "Only sending the employment contract", "Scheduling the end-of-probation review"],
        "correct_answer": "Preparing the workspace, IT access, welcome materials and notifying the team of the new hire's arrival"
    },
    {
        "question": "An effective onboarding checklist ensures:",
        "options": ["The process is completed as quickly as possible", "All essential activities are completed systematically and no critical steps are missed", "Only compliance training is covered", "The employee is assessed for suitability during the first week"],
        "correct_answer": "All essential activities are completed systematically and no critical steps are missed"
    },
    {
        "question": "Creating an engaging onboarding programme involves:",
        "options": ["Providing only written policy documents to read", "Combining interactive activities, early wins, team introductions and meaningful work to build connection and confidence", "Limiting the new employee's interactions in the first week", "Focusing exclusively on compliance and administrative tasks"],
        "correct_answer": "Combining interactive activities, early wins, team introductions and meaningful work to build connection and confidence"
    },
    {
        "question": "Setting expectations during onboarding helps new employees by:",
        "options": ["Reducing the need for any further communication from the manager", "Providing clarity on their role, responsibilities, performance standards and how success will be measured from day one", "Eliminating the need for a probation period", "Replacing the need for a formal job description"],
        "correct_answer": "Providing clarity on their role, responsibilities, performance standards and how success will be measured from day one"
    },
    {
        "question": "Providing feedback to new employees during onboarding is important because:",
        "options": ["It replaces the need for a formal performance review", "Early, constructive feedback helps new employees adjust their behaviour, build confidence and improve performance quickly", "Feedback should only be given at the end of the probation period", "New employees should not receive critical feedback in their first month"],
        "correct_answer": "Early, constructive feedback helps new employees adjust their behaviour, build confidence and improve performance quickly"
    },
    {
        "question": "Following up with new employees after their first few weeks is important to:",
        "options": ["Assess whether they should be retained", "Identify any challenges, provide support and reinforce their sense of belonging and commitment to the organisation", "Complete the remaining compliance training", "Reduce the manager's involvement in the onboarding process"],
        "correct_answer": "Identify any challenges, provide support and reinforce their sense of belonging and commitment to the organisation"
    },
    {
        "question": "HR policies in an organisation serve to:",
        "options": ["Restrict employee freedom unnecessarily", "Provide clear guidelines on expected behaviour, entitlements and procedures, ensuring consistency and fairness across the organisation", "Replace the need for employment contracts", "Only protect the organisation from legal liability"],
        "correct_answer": "Provide clear guidelines on expected behaviour, entitlements and procedures, ensuring consistency and fairness across the organisation"
    },
    {
        "question": "An organisational structure defines:",
        "options": ["The company's product range and pricing strategy", "How roles, responsibilities and reporting relationships are arranged to enable the organisation to achieve its objectives", "The physical layout of the company's offices", "The company's financial reporting hierarchy only"],
        "correct_answer": "How roles, responsibilities and reporting relationships are arranged to enable the organisation to achieve its objectives"
    },
    {
        "question": "Bands and grades in an HR structure are used to:",
        "options": ["Rank employees by performance only", "Create a framework for job levels, pay ranges and career progression that provides clarity and consistency across the organisation", "Determine the number of employees in each department", "Set the annual training budget"],
        "correct_answer": "Create a framework for job levels, pay ranges and career progression that provides clarity and consistency across the organisation"
    },
    {
        "question": "A flat organisational structure is characterised by:",
        "options": ["Many layers of management between the CEO and frontline employees", "Few levels of management, wider spans of control and faster decision-making", "Strict hierarchical reporting with limited employee autonomy", "Separate divisions with their own HR and finance functions"],
        "correct_answer": "Few levels of management, wider spans of control and faster decision-making"
    },
    {
        "question": "The need for HR policies arises from:",
        "options": ["The desire to control all employee behaviour", "The requirement to provide consistent, fair and legally compliant guidance on employment matters across the organisation", "Only legal compliance requirements", "The HR department's preference for documentation"],
        "correct_answer": "The requirement to provide consistent, fair and legally compliant guidance on employment matters across the organisation"
    },
    {
        "question": "Setting up a company's policy framework involves:",
        "options": ["Copying policies from other organisations without adaptation", "Identifying the key areas requiring policy guidance, drafting clear policies aligned to legislation and business values, and communicating them to all employees", "Only creating a disciplinary policy", "Delegating all policy creation to external legal advisors"],
        "correct_answer": "Identifying the key areas requiring policy guidance, drafting clear policies aligned to legislation and business values, and communicating them to all employees"
    },
    {
        "question": "Essential HR systems in an organisation include:",
        "options": ["Only the payroll system", "Recruitment, onboarding, performance management, learning and development, and employee relations systems", "Only compliance and legal management systems", "Only the HR information system (HRIS)"],
        "correct_answer": "Recruitment, onboarding, performance management, learning and development, and employee relations systems"
    },
    {
        "question": "Designing an effective organisational structure requires consideration of:",
        "options": ["Only the number of employees in the organisation", "The business strategy, span of control, decision-making speed, communication flow and the need for specialisation versus flexibility", "Only the CEO's management preferences", "Only the company's current headcount and budget"],
        "correct_answer": "The business strategy, span of control, decision-making speed, communication flow and the need for specialisation versus flexibility"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    # Course 54: Onboarding Principles for Employees
    course54 = await db.courses.find_one({"title": {"$regex": "onboarding principles", "$options": "i"}})
    if course54:
        print(f"Found: {course54['title']}")
        module = await db.modules.find_one({"course_id": course54["id"]})
        existing = await db.quizzes.find_one({"module_id": module["id"]})
        if existing:
            await db.quizzes.delete_one({"module_id": module["id"]})
        await db.quizzes.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "course_id": course54["id"],
            "title": "Onboarding Principles for Employees - Final Assessment",
            "description": "Test your knowledge of onboarding principles, preparation, checklists, feedback and employee integration. You need 70% to pass.",
            "passing_score": 70,
            "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS[:8])]
        })
        print(f"Added quiz with 8 questions to '{course54['title']}'")
    else:
        print("Onboarding Principles course not found")

    # Course 55: Human Resource Policies and Organization Structure
    course55 = await db.courses.find_one({"title": {"$regex": "human resource policies", "$options": "i"}})
    if course55:
        print(f"Found: {course55['title']}")
        module = await db.modules.find_one({"course_id": course55["id"]})
        existing = await db.quizzes.find_one({"module_id": module["id"]})
        if existing:
            await db.quizzes.delete_one({"module_id": module["id"]})
        await db.quizzes.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "course_id": course55["id"],
            "title": "Human Resource Policies and Organization Structure - Final Assessment",
            "description": "Test your knowledge of HR policies, organisational structure, bands and grades and essential HR systems. You need 70% to pass.",
            "passing_score": 70,
            "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS[7:])]
        })
        print(f"Added quiz with {len(QUESTIONS[7:])} questions to '{course55['title']}'")
    else:
        print("HR Policies course not found")

    client.close()

if __name__ == "__main__":
    asyncio.run(add())
