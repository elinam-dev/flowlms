import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "HR analytics is defined as:",
        "options": ["The use of spreadsheets to track employee attendance", "The application of data analysis and statistical methods to HR data to generate insights that improve people decisions and organisational performance", "The process of conducting employee surveys only", "The automation of HR administrative tasks"],
        "correct_answer": "The application of data analysis and statistical methods to HR data to generate insights that improve people decisions and organisational performance"
    },
    {
        "question": "Descriptive HR analytics focuses on:",
        "options": ["Predicting future workforce trends", "Summarising and reporting what has happened in the past using historical HR data", "Prescribing actions to improve HR outcomes", "Diagnosing the root causes of HR problems"],
        "correct_answer": "Summarising and reporting what has happened in the past using historical HR data"
    },
    {
        "question": "Predictive HR analytics is used to:",
        "options": ["Report on past HR performance only", "Forecast future outcomes such as employee turnover, performance or flight risk using statistical models", "Automate HR processes", "Conduct employee satisfaction surveys"],
        "correct_answer": "Forecast future outcomes such as employee turnover, performance or flight risk using statistical models"
    },
    {
        "question": "Prescriptive HR analytics goes beyond prediction by:",
        "options": ["Only identifying what happened in the past", "Recommending specific actions that should be taken to achieve desired HR outcomes", "Describing current workforce demographics", "Automating all HR decisions"],
        "correct_answer": "Recommending specific actions that should be taken to achieve desired HR outcomes"
    },
    {
        "question": "A key HR metric for measuring recruitment effectiveness is:",
        "options": ["Employee net promoter score", "Time-to-fill — the number of days from job opening to accepted offer", "Training completion rate", "Absenteeism rate"],
        "correct_answer": "Time-to-fill — the number of days from job opening to accepted offer"
    },
    {
        "question": "Employee turnover rate is calculated as:",
        "options": ["Number of new hires divided by total headcount", "Number of employees who left during a period divided by average headcount, multiplied by 100", "Total salary cost divided by number of employees", "Number of vacancies divided by total headcount"],
        "correct_answer": "Number of employees who left during a period divided by average headcount, multiplied by 100"
    },
    {
        "question": "HR data quality is important because:",
        "options": ["Poor data quality has no impact on HR decisions", "Inaccurate or incomplete data leads to flawed analysis and poor people decisions that can harm the organisation", "HR data only needs to be accurate for payroll purposes", "Data quality is only relevant for large organisations"],
        "correct_answer": "Inaccurate or incomplete data leads to flawed analysis and poor people decisions that can harm the organisation"
    },
    {
        "question": "A Human Resource Information System (HRIS) supports HR analytics by:",
        "options": ["Replacing the need for HR professionals", "Centralising and storing employee data that can be extracted and analysed to generate workforce insights", "Only processing payroll transactions", "Managing only recruitment activities"],
        "correct_answer": "Centralising and storing employee data that can be extracted and analysed to generate workforce insights"
    },
    {
        "question": "Workforce planning analytics helps organisations to:",
        "options": ["Only track current headcount", "Forecast future talent needs, identify skills gaps and plan hiring, development and succession to meet strategic objectives", "Set the annual HR budget only", "Monitor employee attendance patterns"],
        "correct_answer": "Forecast future talent needs, identify skills gaps and plan hiring, development and succession to meet strategic objectives"
    },
    {
        "question": "Engagement analytics in HR measures:",
        "options": ["Only employee attendance and punctuality", "The level of employee commitment, motivation and connection to the organisation using survey data and behavioural indicators", "Only financial performance metrics", "The number of training courses completed"],
        "correct_answer": "The level of employee commitment, motivation and connection to the organisation using survey data and behavioural indicators"
    },
    {
        "question": "The business value of HR analytics lies in its ability to:",
        "options": ["Replace all HR professionals with data scientists", "Enable evidence-based people decisions that improve performance, reduce costs and create competitive advantage", "Automate all HR processes", "Eliminate the need for employee feedback"],
        "correct_answer": "Enable evidence-based people decisions that improve performance, reduce costs and create competitive advantage"
    },
    {
        "question": "Absenteeism analytics can help organisations to:",
        "options": ["Only track sick days for payroll purposes", "Identify patterns, root causes and high-risk groups to implement targeted interventions that reduce absence and its costs", "Automatically discipline employees with high absence", "Replace the need for occupational health support"],
        "correct_answer": "Identify patterns, root causes and high-risk groups to implement targeted interventions that reduce absence and its costs"
    },
    {
        "question": "Data privacy and ethics in HR analytics requires:",
        "options": ["Sharing all employee data freely across the organisation", "Ensuring employee data is collected, stored and used in compliance with data protection legislation and ethical standards", "Using employee data without their knowledge", "Only senior HR staff having access to all employee data"],
        "correct_answer": "Ensuring employee data is collected, stored and used in compliance with data protection legislation and ethical standards"
    },
    {
        "question": "A people dashboard in HR analytics provides:",
        "options": ["A list of all employee personal details", "A visual summary of key workforce metrics that enables HR and business leaders to monitor performance and make informed decisions", "Only financial HR cost data", "A record of all disciplinary actions taken"],
        "correct_answer": "A visual summary of key workforce metrics that enables HR and business leaders to monitor performance and make informed decisions"
    },
    {
        "question": "The ultimate goal of HR analytics is to:",
        "options": ["Replace human judgement in all HR decisions", "Harness HR data to drive better people decisions, improve organisational performance and demonstrate the strategic value of HR", "Reduce the HR team's headcount through automation", "Focus exclusively on cost reduction in people management"],
        "correct_answer": "Harness HR data to drive better people decisions, improve organisational performance and demonstrate the strategic value of HR"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "HR Analytics", "$options": "i"}})
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
        "title": "HR Analytics - Final Assessment",
        "description": "Test your knowledge of HR analytics, workforce metrics, predictive analytics and data-driven people decisions. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
