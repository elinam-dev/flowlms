import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Strategic performance management links individual and team performance to:",
        "options": ["Only the HR department's objectives", "The overall strategic goals and vision of the organisation", "The annual salary review process only", "The company's marketing strategy exclusively"],
        "correct_answer": "The overall strategic goals and vision of the organisation"
    },
    {
        "question": "The Balanced Scorecard approach to strategic performance management measures performance across:",
        "options": ["Financial results only", "Financial, Customer, Internal Processes and Learning & Growth perspectives", "Employee satisfaction and retention only", "Sales revenue and market share only"],
        "correct_answer": "Financial, Customer, Internal Processes and Learning & Growth perspectives"
    },
    {
        "question": "Strategy mapping in performance management is used to:",
        "options": ["Create the company's organisational chart", "Visually show the cause-and-effect relationships between strategic objectives across different perspectives", "Map employee locations across offices", "Plan the annual training calendar"],
        "correct_answer": "Visually show the cause-and-effect relationships between strategic objectives across different perspectives"
    },
    {
        "question": "Key Performance Indicators (KPIs) in strategic performance management should be:",
        "options": ["As numerous as possible to cover all activities", "Directly linked to strategic objectives, measurable, actionable and limited in number", "Set by employees themselves without management input", "Changed every month to reflect current priorities"],
        "correct_answer": "Directly linked to strategic objectives, measurable, actionable and limited in number"
    },
    {
        "question": "Cascading goals in strategic performance management means:",
        "options": ["Reducing goals at each level of the organisation", "Breaking down organisational strategic objectives into department, team and individual goals that align upward", "Sharing goals only with senior management", "Setting goals only at the end of the financial year"],
        "correct_answer": "Breaking down organisational strategic objectives into department, team and individual goals that align upward"
    },
    {
        "question": "A leading indicator in performance management is:",
        "options": ["A measure of past performance outcomes", "A forward-looking metric that predicts future performance and enables proactive management", "A financial result reported at year end", "A measure of employee satisfaction only"],
        "correct_answer": "A forward-looking metric that predicts future performance and enables proactive management"
    },
    {
        "question": "A lagging indicator in performance management is:",
        "options": ["A metric that predicts future outcomes", "A measure of past results such as revenue, profit or customer retention rate", "A real-time operational metric", "A measure of employee engagement"],
        "correct_answer": "A measure of past results such as revenue, profit or customer retention rate"
    },
    {
        "question": "Performance dashboards in strategic management are used to:",
        "options": ["Replace all written performance reports", "Provide a visual, real-time overview of key performance metrics to support management decision-making", "Track only financial performance", "Monitor employee attendance"],
        "correct_answer": "Provide a visual, real-time overview of key performance metrics to support management decision-making"
    },
    {
        "question": "The purpose of a performance review in strategic performance management is to:",
        "options": ["Determine salary increases only", "Assess progress against strategic objectives, identify barriers and agree on actions to improve performance", "Conduct disciplinary proceedings", "Replace the need for ongoing feedback"],
        "correct_answer": "Assess progress against strategic objectives, identify barriers and agree on actions to improve performance"
    },
    {
        "question": "High-performance culture in an organisation is characterised by:",
        "options": ["Strict top-down control with no employee input", "Clear goals, accountability, continuous feedback, recognition and a commitment to development at all levels", "Focusing only on financial results", "Avoiding all forms of performance measurement"],
        "correct_answer": "Clear goals, accountability, continuous feedback, recognition and a commitment to development at all levels"
    },
    {
        "question": "Succession planning as part of strategic performance management involves:",
        "options": ["Planning the company's product succession strategy", "Identifying and developing internal talent to fill critical leadership and key roles in the future", "Replacing all senior managers with external hires", "Planning employee redundancies"],
        "correct_answer": "Identifying and developing internal talent to fill critical leadership and key roles in the future"
    },
    {
        "question": "Benchmarking in strategic performance management involves:",
        "options": ["Setting performance targets based only on last year's results", "Comparing the organisation's performance against industry best practices or competitors to identify improvement opportunities", "Measuring only internal performance without external reference", "Setting the lowest acceptable performance standard"],
        "correct_answer": "Comparing the organisation's performance against industry best practices or competitors to identify improvement opportunities"
    },
    {
        "question": "The role of leadership in strategic performance management is to:",
        "options": ["Delegate all performance management responsibilities to HR", "Set the strategic direction, model the desired behaviours, hold teams accountable and create conditions for high performance", "Focus only on financial results", "Conduct all performance reviews personally"],
        "correct_answer": "Set the strategic direction, model the desired behaviours, hold teams accountable and create conditions for high performance"
    },
    {
        "question": "Reward and recognition linked to strategic performance management should:",
        "options": ["Be based solely on seniority and tenure", "Reinforce the behaviours and outcomes that drive strategic success, motivating employees to perform at their best", "Be given equally to all employees regardless of performance", "Be limited to financial bonuses only"],
        "correct_answer": "Reinforce the behaviours and outcomes that drive strategic success, motivating employees to perform at their best"
    },
    {
        "question": "Which of the following best describes the strategic value of an effective performance management system?",
        "options": ["It reduces the HR department's administrative burden only", "It drives organisational performance by aligning people, processes and resources with strategic priorities", "It eliminates the need for organisational strategy", "It focuses exclusively on managing underperformance"],
        "correct_answer": "It drives organisational performance by aligning people, processes and resources with strategic priorities"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "diploma in strategic performance", "$options": "i"}})
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
        "title": "Diploma in Strategic Performance Management - Final Assessment",
        "description": "Test your knowledge of strategic performance management, Balanced Scorecard, KPIs, cascading goals and high-performance culture. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
