import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "What is the primary focus of throughput accounting?",
        "options": ["Minimizing overhead costs", "Maximizing the rate at which a system generates money through sales", "Reducing labor costs per unit", "Allocating fixed costs to products"],
        "correct_answer": "Maximizing the rate at which a system generates money through sales"
    },
    {
        "question": "In throughput accounting, which of the following is classified as a Totally Variable Cost (TVC)?",
        "options": ["Rent", "Salaries", "Direct materials", "Utilities"],
        "correct_answer": "Direct materials"
    },
    {
        "question": "Throughput Contribution is calculated as:",
        "options": ["Sales Revenue − Operating Expenses", "Sales Revenue − Total Variable Costs", "Gross Profit − Overheads", "Net Profit + Depreciation"],
        "correct_answer": "Sales Revenue − Total Variable Costs"
    },
    {
        "question": "Which concept is central to the Theory of Constraints (TOC), which underpins throughput accounting?",
        "options": ["Activity-based costing", "The bottleneck resource", "Standard costing variances", "Absorption of fixed overheads"],
        "correct_answer": "The bottleneck resource"
    },
    {
        "question": "In throughput accounting, inventory is treated as:",
        "options": ["An asset that adds value", "A liability to be minimized", "A source of profit", "A fixed cost driver"],
        "correct_answer": "A liability to be minimized"
    },
    {
        "question": "The Throughput Accounting Ratio (TA Ratio) is calculated as:",
        "options": ["Throughput / Operating Expenses", "Net Profit / Sales", "Throughput per bottleneck unit / Operating cost per bottleneck unit", "Sales / Total Variable Costs"],
        "correct_answer": "Throughput per bottleneck unit / Operating cost per bottleneck unit"
    },
    {
        "question": "Which of the following best describes lean accounting?",
        "options": ["A system focused on maximizing absorption of overheads", "An accounting approach aligned with lean manufacturing principles to eliminate waste", "A method of calculating standard costs for mass production", "A tax reporting framework for manufacturing firms"],
        "correct_answer": "An accounting approach aligned with lean manufacturing principles to eliminate waste"
    },
    {
        "question": "In lean accounting, costs are tracked by:",
        "options": ["Individual departments", "Product lines only", "Value streams", "Cost centers"],
        "correct_answer": "Value streams"
    },
    {
        "question": "Which of the following is a key waste (muda) that lean accounting aims to eliminate?",
        "options": ["Accurate financial reporting", "Excessive variance analysis that doesn't drive decisions", "Value stream mapping", "Customer invoicing"],
        "correct_answer": "Excessive variance analysis that doesn't drive decisions"
    },
    {
        "question": "A company has Sales of $500,000, Totally Variable Costs of $200,000, and Operating Expenses of $250,000. What is the Net Profit under throughput accounting?",
        "options": ["$300,000", "$50,000", "$250,000", "$150,000"],
        "correct_answer": "$50,000"
    },
    {
        "question": "Which statement best distinguishes throughput accounting from absorption costing?",
        "options": ["Throughput accounting allocates fixed costs to products; absorption costing does not", "Absorption costing can encourage overproduction; throughput accounting discourages it", "Throughput accounting is only used in service industries", "Absorption costing focuses on bottleneck resources"],
        "correct_answer": "Absorption costing can encourage overproduction; throughput accounting discourages it"
    },
    {
        "question": "In lean accounting, a 'box score' report typically includes:",
        "options": ["Tax liabilities and audit findings", "Operational, capacity, and financial metrics for a value stream", "Individual employee performance data", "Standard cost variances by department"],
        "correct_answer": "Operational, capacity, and financial metrics for a value stream"
    },
    {
        "question": "Which of the following actions would throughput accounting prioritize first when facing a bottleneck?",
        "options": ["Hire more staff across all departments", "Exploit the bottleneck to its maximum capacity", "Reduce the selling price to increase volume", "Outsource the entire production process"],
        "correct_answer": "Exploit the bottleneck to its maximum capacity"
    },
    {
        "question": "Lean accounting supports decision-making by:",
        "options": ["Providing detailed standard cost reports monthly", "Delivering timely, visual, and relevant information to operational teams", "Focusing exclusively on financial KPIs", "Replacing all management reports with tax summaries"],
        "correct_answer": "Delivering timely, visual, and relevant information to operational teams"
    },
    {
        "question": "Product A has a throughput of $80 and requires 4 minutes of bottleneck time. Product B has a throughput of $60 and requires 2 minutes. Which should be prioritized?",
        "options": ["Product A, because it has higher total throughput", "Product B, because it generates $30 per bottleneck minute vs. $20", "Product A, because it uses more bottleneck time", "Both equally, as total throughput is what matters"],
        "correct_answer": "Product B, because it generates $30 per bottleneck minute vs. $20"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    course = await db.courses.find_one({"title": {"$regex": "throughput", "$options": "i"}})
    if not course:
        print("Course not found")
        return

    print(f"Found course: {course['title']}")

    module = await db.modules.find_one({"course_id": course["id"]})
    if not module:
        print("Module not found")
        return

    existing = await db.quizzes.find_one({"module_id": module["id"]})
    if existing:
        await db.quizzes.delete_one({"module_id": module["id"]})
        print("Removed existing quiz")

    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module["id"],
        "course_id": course["id"],
        "title": "Throughput Accounting & Lean Accounting – Final Assessment",
        "description": "Test your understanding of throughput accounting, the Theory of Constraints, and lean accounting principles. You need 70% to pass.",
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
