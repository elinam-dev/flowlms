import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "The primary purpose of employee onboarding is to:",
        "options": ["Complete administrative paperwork as quickly as possible", "Help new employees integrate into the organisation, understand their role and become productive contributors", "Assess whether the new hire was the right choice", "Introduce the employee to the payroll system only"],
        "correct_answer": "Help new employees integrate into the organisation, understand their role and become productive contributors"
    },
    {
        "question": "Research shows that effective onboarding programmes improve:",
        "options": ["Only the speed of administrative processing", "New employee retention, time-to-productivity and overall job satisfaction", "Only the HR department's efficiency", "The company's marketing performance"],
        "correct_answer": "New employee retention, time-to-productivity and overall job satisfaction"
    },
    {
        "question": "Pre-boarding refers to:",
        "options": ["The interview process before a job offer", "Activities and communications that engage the new hire between accepting the offer and their first day", "The probation period after joining", "The induction training on the first day only"],
        "correct_answer": "Activities and communications that engage the new hire between accepting the offer and their first day"
    },
    {
        "question": "Maslow's Hierarchy of Needs suggests that employees are motivated by:",
        "options": ["Only financial rewards", "A progression of needs from basic physiological needs through safety, belonging, esteem to self-actualisation", "Competition with colleagues only", "Fear of job loss exclusively"],
        "correct_answer": "A progression of needs from basic physiological needs through safety, belonging, esteem to self-actualisation"
    },
    {
        "question": "Intrinsic motivation in the workplace refers to:",
        "options": ["Motivation driven by external rewards such as salary and bonuses", "Motivation that comes from within — driven by personal satisfaction, purpose and the enjoyment of the work itself", "Motivation driven by fear of disciplinary action", "Motivation from peer recognition only"],
        "correct_answer": "Motivation that comes from within — driven by personal satisfaction, purpose and the enjoyment of the work itself"
    },
    {
        "question": "Herzberg's Two-Factor Theory distinguishes between:",
        "options": ["Intrinsic and extrinsic motivation only", "Hygiene factors that prevent dissatisfaction and motivators that actively drive satisfaction and engagement", "Short-term and long-term motivation", "Individual and team motivation"],
        "correct_answer": "Hygiene factors that prevent dissatisfaction and motivators that actively drive satisfaction and engagement"
    },
    {
        "question": "Which of the following is an example of a hygiene factor according to Herzberg?",
        "options": ["Recognition for achievement", "Opportunities for growth and advancement", "Salary and working conditions", "Meaningful and challenging work"],
        "correct_answer": "Salary and working conditions"
    },
    {
        "question": "A buddy system during onboarding is designed to:",
        "options": ["Monitor the new employee's performance", "Pair the new hire with an experienced colleague who provides informal support, guidance and social integration", "Assign additional work to the new employee", "Replace the line manager's role during induction"],
        "correct_answer": "Pair the new hire with an experienced colleague who provides informal support, guidance and social integration"
    },
    {
        "question": "Setting clear expectations during onboarding helps new employees by:",
        "options": ["Reducing the need for any further communication", "Providing clarity on their role, responsibilities, performance standards and how success will be measured", "Eliminating the need for a probation period", "Replacing the need for a job description"],
        "correct_answer": "Providing clarity on their role, responsibilities, performance standards and how success will be measured"
    },
    {
        "question": "Employee engagement during onboarding is best supported by:",
        "options": ["Providing only written manuals and policy documents", "Creating interactive experiences, early wins, meaningful connections and a sense of belonging from day one", "Limiting contact with the team during the first week", "Focusing exclusively on compliance training"],
        "correct_answer": "Creating interactive experiences, early wins, meaningful connections and a sense of belonging from day one"
    },
    {
        "question": "The 30-60-90 day onboarding plan is used to:",
        "options": ["Set the employee's salary review schedule", "Structure the new employee's learning, integration and performance milestones across the first three months", "Plan the employee's annual leave", "Schedule all compliance training in the first week"],
        "correct_answer": "Structure the new employee's learning, integration and performance milestones across the first three months"
    },
    {
        "question": "Which motivational theory focuses on employees' need for Autonomy, Mastery and Purpose?",
        "options": ["Maslow's Hierarchy of Needs", "Herzberg's Two-Factor Theory", "Daniel Pink's Self-Determination Theory", "McGregor's Theory X and Theory Y"],
        "correct_answer": "Daniel Pink's Self-Determination Theory"
    },
    {
        "question": "Manager involvement in onboarding is critical because:",
        "options": ["It reduces the HR team's workload", "The direct manager has the greatest influence on a new employee's experience, engagement and early performance", "It replaces the need for a formal induction programme", "It ensures compliance with company policies only"],
        "correct_answer": "The direct manager has the greatest influence on a new employee's experience, engagement and early performance"
    },
    {
        "question": "Following up with new employees after their first few weeks is important to:",
        "options": ["Check if they have completed all paperwork", "Identify any challenges, provide support and reinforce their sense of belonging and commitment to the organisation", "Assess whether they should be retained", "Reduce the frequency of future check-ins"],
        "correct_answer": "Identify any challenges, provide support and reinforce their sense of belonging and commitment to the organisation"
    },
    {
        "question": "A motivated workforce contributes to organisational success by:",
        "options": ["Reducing the need for performance management", "Delivering higher productivity, better quality work, lower absenteeism and stronger employee retention", "Eliminating the need for competitive salaries", "Reducing the need for training and development"],
        "correct_answer": "Delivering higher productivity, better quality work, lower absenteeism and stronger employee retention"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "employee onboarding and motivation", "$options": "i"}})
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
        "title": "Employee Onboarding and Motivation - Final Assessment",
        "description": "Test your knowledge of onboarding best practices, motivation theories and employee engagement strategies. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
