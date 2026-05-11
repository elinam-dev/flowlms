import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "A Performance Management System (PMS) is designed to:",
        "options": ["Replace the annual appraisal with a one-time review", "Continuously align individual performance with organisational goals through planning, monitoring, feedback and development", "Track employee attendance only", "Manage payroll and compensation exclusively"],
        "correct_answer": "Continuously align individual performance with organisational goals through planning, monitoring, feedback and development"
    },
    {
        "question": "The first step in designing an effective performance management system is:",
        "options": ["Distributing appraisal forms to all employees", "Defining clear organisational goals and cascading them into individual performance objectives", "Conducting annual salary reviews", "Identifying underperforming employees"],
        "correct_answer": "Defining clear organisational goals and cascading them into individual performance objectives"
    },
    {
        "question": "SMART goals in performance management stand for:",
        "options": ["Simple, Measurable, Achievable, Relevant, Timely", "Specific, Measurable, Achievable, Relevant, Time-bound", "Strategic, Managed, Assessed, Reviewed, Tracked", "Structured, Monitored, Aligned, Realistic, Targeted"],
        "correct_answer": "Specific, Measurable, Achievable, Relevant, Time-bound"
    },
    {
        "question": "Key Result Areas (KRAs) in a performance management system define:",
        "options": ["The employee's salary band", "The primary areas of responsibility where an employee is expected to deliver results", "The company's financial targets only", "The training budget for each department"],
        "correct_answer": "The primary areas of responsibility where an employee is expected to deliver results"
    },
    {
        "question": "360-degree feedback in performance management involves collecting feedback from:",
        "options": ["Only the direct line manager", "The employee's manager, peers, direct reports and sometimes customers", "Only the HR department", "Only senior leadership"],
        "correct_answer": "The employee's manager, peers, direct reports and sometimes customers"
    },
    {
        "question": "Continuous performance management differs from traditional annual appraisals in that it:",
        "options": ["Eliminates all formal reviews", "Involves regular check-ins, ongoing feedback and real-time goal adjustments throughout the year", "Only focuses on end-of-year ratings", "Removes manager involvement from the process"],
        "correct_answer": "Involves regular check-ins, ongoing feedback and real-time goal adjustments throughout the year"
    },
    {
        "question": "A performance improvement plan (PIP) is used when:",
        "options": ["An employee exceeds all performance targets", "An employee's performance falls below the required standard and structured support is needed to improve it", "A new employee joins the organisation", "An employee requests a promotion"],
        "correct_answer": "An employee's performance falls below the required standard and structured support is needed to improve it"
    },
    {
        "question": "Calibration sessions in performance management are conducted to:",
        "options": ["Train managers on how to use the HR system", "Ensure consistency and fairness in performance ratings across different managers and departments", "Set the annual salary budget", "Conduct exit interviews"],
        "correct_answer": "Ensure consistency and fairness in performance ratings across different managers and departments"
    },
    {
        "question": "Which of the following is a key principle of effective performance feedback?",
        "options": ["Feedback should only be given during the annual review", "Feedback should be specific, timely, balanced and focused on behaviour and outcomes rather than personality", "Feedback should always be positive to maintain morale", "Feedback should only address negative performance"],
        "correct_answer": "Feedback should be specific, timely, balanced and focused on behaviour and outcomes rather than personality"
    },
    {
        "question": "Linking performance management to learning and development ensures:",
        "options": ["Employees are only rewarded financially", "Performance gaps identified during reviews are addressed through targeted training and development plans", "All employees receive the same training regardless of performance", "Development plans are created only for high performers"],
        "correct_answer": "Performance gaps identified during reviews are addressed through targeted training and development plans"
    },
    {
        "question": "The purpose of a mid-year performance review is to:",
        "options": ["Replace the end-of-year appraisal", "Check progress against goals, address obstacles and adjust objectives if business priorities have changed", "Determine salary increases for the year", "Conduct disciplinary proceedings"],
        "correct_answer": "Check progress against goals, address obstacles and adjust objectives if business priorities have changed"
    },
    {
        "question": "OKRs (Objectives and Key Results) in performance management are used to:",
        "options": ["Track employee attendance and punctuality", "Set ambitious goals and define measurable outcomes that indicate whether the objective has been achieved", "Replace all other performance metrics", "Manage employee benefits and compensation"],
        "correct_answer": "Set ambitious goals and define measurable outcomes that indicate whether the objective has been achieved"
    },
    {
        "question": "A well-designed performance management system should be:",
        "options": ["Focused only on identifying poor performers", "Transparent, fair, consistent and aligned with both individual development and organisational strategy", "Managed exclusively by the HR department without manager involvement", "Conducted only once per year with no interim touchpoints"],
        "correct_answer": "Transparent, fair, consistent and aligned with both individual development and organisational strategy"
    },
    {
        "question": "Which of the following is a common pitfall in performance management systems?",
        "options": ["Setting clear and measurable goals", "Recency bias — where managers rate employees based only on recent performance rather than the full review period", "Providing regular feedback throughout the year", "Linking performance to development opportunities"],
        "correct_answer": "Recency bias — where managers rate employees based only on recent performance rather than the full review period"
    },
    {
        "question": "The role of HR in a performance management system is to:",
        "options": ["Conduct all performance reviews on behalf of line managers", "Design, implement and maintain the system, train managers and ensure consistency and compliance across the organisation", "Set individual performance targets for every employee", "Approve all salary increases independently"],
        "correct_answer": "Design, implement and maintain the system, train managers and ensure consistency and compliance across the organisation"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "how to design performance", "$options": "i"}})
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
        "title": "How to Design a Performance Management System - Final Assessment",
        "description": "Test your knowledge of PMS design, SMART goals, KRAs, feedback and continuous performance management. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
