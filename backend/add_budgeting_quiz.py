import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "6baf5c3e-6b9d-490b-a67e-ebf2a2533b73"

QUESTIONS = [
    {
        "question": "What is the primary purpose of a budget in an organisation?",
        "options": ["To record past financial transactions", "To plan, coordinate and control future financial activities", "To calculate tax liabilities", "To prepare audit reports"],
        "correct_answer": "To plan, coordinate and future financial activities"
    },
    {
        "question": "Which of the following best describes budgetary control?",
        "options": ["Comparing actual results with budgeted figures and taking corrective action", "Preparing financial statements at year end", "Setting prices for products and services", "Calculating depreciation on fixed assets"],
        "correct_answer": "Comparing actual results with budgeted figures and taking corrective action"
    },
    {
        "question": "A cash budget is primarily used to:",
        "options": ["Determine product profitability", "Forecast cash inflows and outflows over a period", "Calculate standard costs", "Measure employee performance"],
        "correct_answer": "Forecast cash inflows and outflows over a period"
    },
    {
        "question": "Which budget is typically prepared first in the budgeting process?",
        "options": ["Production budget", "Cash budget", "Sales budget", "Labour budget"],
        "correct_answer": "Sales budget"
    },
    {
        "question": "Standard costing is best described as:",
        "options": ["Recording actual costs incurred during production", "Setting predetermined costs against which actual costs are compared", "Calculating the total cost of a project after completion", "Estimating tax payable at year end"],
        "correct_answer": "Setting predetermined costs against which actual costs are compared"
    },
    {
        "question": "A favourable variance occurs when:",
        "options": ["Actual costs exceed budgeted costs", "Actual revenue is less than budgeted revenue", "Actual costs are less than budgeted costs", "The budget is not achieved"],
        "correct_answer": "Actual costs are less than budgeted costs"
    },
    {
        "question": "Material Price Variance measures the difference between:",
        "options": ["Actual quantity used and standard quantity allowed", "Actual price paid and standard price for the actual quantity purchased", "Budgeted material cost and actual material cost", "Standard usage and actual usage at standard price"],
        "correct_answer": "Actual price paid and standard price for the actual quantity purchased"
    },
    {
        "question": "Material Usage Variance is calculated as:",
        "options": ["(Actual price - Standard price) x Actual quantity", "(Standard quantity for actual output - Actual quantity used) x Standard price", "Actual cost - Budgeted cost", "(Actual hours - Standard hours) x Standard rate"],
        "correct_answer": "(Standard quantity for actual output - Actual quantity used) x Standard price"
    },
    {
        "question": "A company budgeted to sell 1,000 units but actually sold 1,200 units. The sales volume variance is:",
        "options": ["Adverse", "Favourable", "Nil", "Cannot be determined"],
        "correct_answer": "Favourable"
    },
    {
        "question": "Labour Efficiency Variance measures:",
        "options": ["The difference between actual wage rate and standard wage rate", "The difference between actual hours worked and standard hours for actual output", "Total labour cost against budget", "Overtime premium paid to workers"],
        "correct_answer": "The difference between actual hours worked and standard hours for actual output"
    },
    {
        "question": "Which of the following is an advantage of budgetary control?",
        "options": ["It eliminates the need for financial statements", "It ensures all employees receive bonuses", "It helps identify inefficiencies and areas needing corrective action", "It removes the need for external audits"],
        "correct_answer": "It helps identify inefficiencies and areas needing corrective action"
    },
    {
        "question": "A material cost variance is adverse when:",
        "options": ["Actual material cost is less than standard material cost", "Actual material cost exceeds standard material cost", "Standard quantity exceeds actual quantity used", "The purchase price falls below standard"],
        "correct_answer": "Actual material cost exceeds standard material cost"
    },
    {
        "question": "Zero-based budgeting (ZBB) requires managers to:",
        "options": ["Increase last year's budget by a fixed percentage", "Justify every item of expenditure from scratch each period", "Only budget for new activities", "Use historical data without revision"],
        "correct_answer": "Justify every item of expenditure from scratch each period"
    },
    {
        "question": "The purpose of a material purchase budget is to:",
        "options": ["Record supplier invoices", "Determine how much raw material needs to be purchased to meet production requirements", "Calculate the cost of goods sold", "Set selling prices for finished goods"],
        "correct_answer": "Determine how much raw material needs to be purchased to meet production requirements"
    },
    {
        "question": "Which statement about variance analysis is correct?",
        "options": ["Only adverse variances need to be investigated", "All variances, both favourable and adverse, may warrant investigation", "Variance analysis is only relevant for large companies", "Favourable variances always indicate good management performance"],
        "correct_answer": "All variances, both favourable and adverse, may warrant investigation"
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
        "title": "Fundamentals of Budgeting and Variance Analysis - Final Assessment",
        "description": "Test your knowledge of budgeting, budgetary control, standard costing and variance analysis. You need 70% to pass.",
        "passing_score": 70,
        "questions": [
            {
                "question": q["question"],
                "question_type": "multiple_choice",
                "options": q["options"],
                "correct_answer": q["correct_answer"],
                "points": 1,
                "order": i
            }
            for i, q in enumerate(QUESTIONS)
        ]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
