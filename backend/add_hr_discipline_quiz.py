import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "The primary purpose of a disciplinary process in the workplace is to:",
        "options": ["Punish employees for misconduct", "Correct unacceptable behaviour or performance and give employees the opportunity to improve", "Create a paper trail for dismissal", "Demonstrate management authority"],
        "correct_answer": "Correct unacceptable behaviour or performance and give employees the opportunity to improve"
    },
    {
        "question": "Progressive discipline refers to:",
        "options": ["Immediately dismissing an employee for any misconduct", "A step-by-step approach that escalates consequences for repeated or serious misconduct, typically from verbal warning to dismissal", "Promoting employees who improve their behaviour", "Conducting disciplinary hearings only for senior staff"],
        "correct_answer": "A step-by-step approach that escalates consequences for repeated or serious misconduct, typically from verbal warning to dismissal"
    },
    {
        "question": "Gross misconduct in the workplace typically refers to:",
        "options": ["Minor performance issues that can be corrected with coaching", "Serious offences such as theft, fraud, violence or gross insubordination that may warrant immediate dismissal", "Repeated lateness over a period of months", "Failure to meet a single performance target"],
        "correct_answer": "Serious offences such as theft, fraud, violence or gross insubordination that may warrant immediate dismissal"
    },
    {
        "question": "Natural justice in a disciplinary process requires that:",
        "options": ["The outcome is always dismissal for serious offences", "The employee is informed of the allegations, given the opportunity to respond and the decision is made impartially", "Only HR staff conduct disciplinary hearings", "Disciplinary decisions are made without informing the employee in advance"],
        "correct_answer": "The employee is informed of the allegations, given the opportunity to respond and the decision is made impartially"
    },
    {
        "question": "A written warning in a disciplinary process should include:",
        "options": ["Only the date of the incident", "A clear description of the misconduct, the expected standard of behaviour, consequences of recurrence and the employee's right to appeal", "Only the manager's signature", "A list of all previous incidents regardless of relevance"],
        "correct_answer": "A clear description of the misconduct, the expected standard of behaviour, consequences of recurrence and the employee's right to appeal"
    },
    {
        "question": "The right to be accompanied during a disciplinary hearing means:",
        "options": ["The employee can bring their lawyer to the hearing", "The employee has the right to be accompanied by a colleague or trade union representative", "The employee can bring any person of their choice including family members", "Only senior employees have this right"],
        "correct_answer": "The employee has the right to be accompanied by a colleague or trade union representative"
    },
    {
        "question": "Unfair dismissal occurs when:",
        "options": ["An employee is dismissed for gross misconduct after a fair process", "An employee is dismissed without a fair reason or without following a fair procedure", "An employee resigns voluntarily", "An employee is made redundant due to business restructuring"],
        "correct_answer": "An employee is dismissed without a fair reason or without following a fair procedure"
    },
    {
        "question": "Constructive dismissal refers to:",
        "options": ["An employer constructively building a case for dismissal over time", "An employee resigning because the employer's conduct has made their position untenable, which may be treated as dismissal", "A mutual agreement to end employment", "A dismissal that is later overturned on appeal"],
        "correct_answer": "An employee resigning because the employer's conduct has made their position untenable, which may be treated as dismissal"
    },
    {
        "question": "Before initiating a disciplinary process, a manager should:",
        "options": ["Immediately issue a written warning", "Investigate the matter thoroughly to establish the facts before taking any formal action", "Consult only with senior management", "Inform all team members of the situation"],
        "correct_answer": "Investigate the matter thoroughly to establish the facts before taking any formal action"
    },
    {
        "question": "Redundancy as a reason for termination is valid when:",
        "options": ["The employer wants to replace an employee with someone cheaper", "The role is no longer required due to genuine business reasons such as restructuring, closure or reduced demand", "The employee has performance issues", "The employer wants to change the employee's terms and conditions"],
        "correct_answer": "The role is no longer required due to genuine business reasons such as restructuring, closure or reduced demand"
    },
    {
        "question": "Documentation in disciplinary proceedings is important because:",
        "options": ["It is only required for senior employees", "It provides a clear record of the process followed, protecting both the employer and employee and supporting any appeal or legal proceedings", "It replaces the need for a formal hearing", "It is only needed if the case goes to tribunal"],
        "correct_answer": "It provides a clear record of the process followed, protecting both the employer and employee and supporting any appeal or legal proceedings"
    },
    {
        "question": "An appeal process in disciplinary matters allows:",
        "options": ["The employee to have the decision reviewed by a more senior manager or independent party", "The employee to restart the entire disciplinary process", "The HR department to overturn any manager's decision", "Only the employer to challenge the outcome"],
        "correct_answer": "The employee to have the decision reviewed by a more senior manager or independent party"
    },
    {
        "question": "Suspension during a disciplinary investigation should be:",
        "options": ["Used as a form of punishment", "A neutral act on full pay while the investigation is conducted, not an indication of guilt", "Unpaid to signal the seriousness of the allegation", "Applied only in cases of gross misconduct"],
        "correct_answer": "A neutral act on full pay while the investigation is conducted, not an indication of guilt"
    },
    {
        "question": "Which of the following is a fair reason for dismissal?",
        "options": ["The employee is pregnant", "The employee has a disability", "The employee's conduct, capability, redundancy, legal restriction or some other substantial reason", "The employee raised a grievance against their manager"],
        "correct_answer": "The employee's conduct, capability, redundancy, legal restriction or some other substantial reason"
    },
    {
        "question": "The role of HR in disciplinary and termination processes is to:",
        "options": ["Make all disciplinary decisions on behalf of line managers", "Advise on policy and procedure, ensure fairness and legal compliance, and support managers in conducting fair processes", "Protect the company from all employee claims regardless of merit", "Conduct all disciplinary hearings independently of line managers"],
        "correct_answer": "Advise on policy and procedure, ensure fairness and legal compliance, and support managers in conducting fair processes"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "discipline and termination", "$options": "i"}})
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
        "title": "Human Resources: Discipline and Termination - Final Assessment",
        "description": "Test your knowledge of disciplinary procedures, fair dismissal, natural justice and termination best practices. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
