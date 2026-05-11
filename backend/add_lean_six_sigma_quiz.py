import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Lean Six Sigma combines two methodologies. What is the primary focus of the 'Lean' component?",
        "options": ["Reducing statistical variation in processes", "Eliminating waste and improving process flow and speed", "Increasing headcount to improve output", "Focusing on financial cost reduction only"],
        "correct_answer": "Eliminating waste and improving process flow and speed"
    },
    {
        "question": "Six Sigma focuses primarily on:",
        "options": ["Speeding up production cycles", "Reducing process variation and defects to improve quality", "Increasing inventory levels", "Expanding market share"],
        "correct_answer": "Reducing process variation and defects to improve quality"
    },
    {
        "question": "The acronym DMAIC in Six Sigma stands for:",
        "options": ["Define, Measure, Analyse, Improve, Control", "Design, Monitor, Assess, Implement, Close", "Detect, Manage, Analyse, Inspect, Correct", "Define, Map, Audit, Improve, Check"],
        "correct_answer": "Define, Measure, Analyse, Improve, Control"
    },
    {
        "question": "In Lean, the 8 wastes are remembered using the acronym DOWNTIME. Which of the following is one of the 8 wastes?",
        "options": ["Delegation", "Overproduction", "Overtime", "Outsourcing"],
        "correct_answer": "Overproduction"
    },
    {
        "question": "A White Belt in Lean Six Sigma is expected to:",
        "options": ["Lead complex improvement projects independently", "Understand basic Lean Six Sigma concepts and support improvement initiatives", "Conduct advanced statistical analysis", "Certify other team members in Six Sigma"],
        "correct_answer": "Understand basic Lean Six Sigma concepts and support improvement initiatives"
    },
    {
        "question": "Value in Lean is defined as:",
        "options": ["Anything that reduces cost for the company", "Any activity or feature for which the customer is willing to pay", "All steps in the production process", "Activities that improve employee satisfaction"],
        "correct_answer": "Any activity or feature for which the customer is willing to pay"
    },
    {
        "question": "A Value Stream Map is used to:",
        "options": ["Track employee performance metrics", "Visualise the flow of materials and information through a process to identify waste and improvement opportunities", "Map the company's organisational structure", "Plan marketing campaigns"],
        "correct_answer": "Visualise the flow of materials and information through a process to identify waste and improvement opportunities"
    },
    {
        "question": "The 5S methodology in Lean stands for:",
        "options": ["Sort, Set in order, Shine, Standardise, Sustain", "Speed, Safety, Simplify, Standardise, Support", "Select, Sequence, Sanitise, Stabilise, Scale", "Scan, Sort, Store, Standardise, Share"],
        "correct_answer": "Sort, Set in order, Shine, Standardise, Sustain"
    },
    {
        "question": "A process operating at Six Sigma quality level produces approximately:",
        "options": ["1,000 defects per million opportunities", "3.4 defects per million opportunities", "10,000 defects per million opportunities", "Zero defects in all circumstances"],
        "correct_answer": "3.4 defects per million opportunities"
    },
    {
        "question": "The 'Define' phase of DMAIC involves:",
        "options": ["Collecting process data and measuring current performance", "Identifying the problem, project scope, customer requirements and project goals", "Implementing the chosen solution", "Monitoring the process after improvement"],
        "correct_answer": "Identifying the problem, project scope, customer requirements and project goals"
    },
    {
        "question": "Kaizen in Lean Six Sigma refers to:",
        "options": ["A one-time large-scale transformation project", "A philosophy of continuous, incremental improvement involving all employees", "A statistical tool for measuring defects", "A Japanese term for waste elimination only"],
        "correct_answer": "A philosophy of continuous, incremental improvement involving all employees"
    },
    {
        "question": "Which of the following best describes a 'defect' in Six Sigma?",
        "options": ["Any product that is returned by a customer", "Any instance where a process output fails to meet customer specifications or requirements", "A machine breakdown during production", "An employee error that is corrected before delivery"],
        "correct_answer": "Any instance where a process output fails to meet customer specifications or requirements"
    },
    {
        "question": "The 'Control' phase of DMAIC is designed to:",
        "options": ["Identify root causes of the problem", "Sustain the improvements made and prevent the process from reverting to its previous state", "Collect baseline data on the process", "Generate potential solutions for the problem"],
        "correct_answer": "Sustain the improvements made and prevent the process from reverting to its previous state"
    },
    {
        "question": "A fishbone (Ishikawa) diagram is used in Six Sigma to:",
        "options": ["Map the flow of a process from start to finish", "Identify and categorise potential root causes of a problem", "Track defect rates over time", "Prioritise improvement projects by financial impact"],
        "correct_answer": "Identify and categorise potential root causes of a problem"
    },
    {
        "question": "Which statement best describes the relationship between Lean and Six Sigma?",
        "options": ["They are competing methodologies that cannot be used together", "Lean focuses on speed and waste elimination while Six Sigma focuses on quality and variation reduction — together they deliver faster, higher-quality processes", "Six Sigma replaces Lean in modern organisations", "Lean is only applicable to manufacturing while Six Sigma applies only to services"],
        "correct_answer": "Lean focuses on speed and waste elimination while Six Sigma focuses on quality and variation reduction — together they deliver faster, higher-quality processes"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "lean.*six.*sigma.*white.*belt", "$options": "i"}})
    if not course:
        course = await db.courses.find_one({"title": {"$regex": "lean.*six.*sigma", "$options": "i"}})
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
        "title": "Lean Six Sigma: White Belt - Final Assessment",
        "description": "Test your understanding of Lean Six Sigma fundamentals including DMAIC, the 8 wastes, 5S and continuous improvement. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
