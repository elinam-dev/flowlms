import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "3e5143d8-e3ff-489a-a728-81d059b85787"

QUESTIONS = [
    {
        "question": "Cost accounting is primarily concerned with:",
        "options": ["Preparing tax returns", "Recording, classifying and analysing costs to aid management decisions", "Auditing financial statements", "Managing accounts receivable"],
        "correct_answer": "Recording, classifying and analysing costs to aid management decisions"
    },
    {
        "question": "Which of the following is a fixed cost?",
        "options": ["Direct materials", "Sales commission", "Factory rent", "Packing materials"],
        "correct_answer": "Factory rent"
    },
    {
        "question": "The Contribution Margin is calculated as:",
        "options": ["Sales Revenue - Total Fixed Costs", "Sales Revenue - Total Variable Costs", "Gross Profit - Operating Expenses", "Net Profit + Depreciation"],
        "correct_answer": "Sales Revenue - Total Variable Costs"
    },
    {
        "question": "The Break-Even Point (BEP) in units is calculated as:",
        "options": ["Fixed Costs / Contribution per unit", "Variable Costs / Selling Price", "Total Costs / Number of units", "Fixed Costs x Contribution Margin Ratio"],
        "correct_answer": "Fixed Costs / Contribution per unit"
    },
    {
        "question": "The P/V Ratio (Profit Volume Ratio) is also known as:",
        "options": ["Gross Profit Ratio", "Contribution Margin Ratio", "Net Profit Ratio", "Operating Leverage Ratio"],
        "correct_answer": "Contribution Margin Ratio"
    },
    {
        "question": "Marginal costing treats fixed production overheads as:",
        "options": ["Product costs absorbed into inventory", "Period costs charged to the income statement", "Capital expenditure", "Deferred expenses"],
        "correct_answer": "Period costs charged to the income statement"
    },
    {
        "question": "A sunk cost is best described as:",
        "options": ["A future cost relevant to a decision", "A cost that has already been incurred and cannot be recovered", "A variable cost that changes with output", "An opportunity cost foregone"],
        "correct_answer": "A cost that has already been incurred and cannot be recovered"
    },
    {
        "question": "Sensitivity analysis in CVP is used to:",
        "options": ["Calculate exact profit figures", "Assess how changes in key variables affect the break-even point and profit", "Prepare cash flow forecasts", "Determine standard costs"],
        "correct_answer": "Assess how changes in key variables affect the break-even point and profit"
    },
    {
        "question": "Which cost classification separates costs based on their behaviour relative to output?",
        "options": ["Direct and indirect costs", "Fixed and variable costs", "Product and period costs", "Capital and revenue costs"],
        "correct_answer": "Fixed and variable costs"
    },
    {
        "question": "A company has fixed costs of $50,000 and a contribution per unit of $25. What is the break-even point in units?",
        "options": ["1,000 units", "2,000 units", "2,500 units", "5,000 units"],
        "correct_answer": "2,000 units"
    },
    {
        "question": "In a make-or-buy decision, which costs are most relevant?",
        "options": ["Sunk costs and fixed overheads", "Incremental (differential) costs and opportunity costs", "Historical costs and depreciation", "Total absorption costs only"],
        "correct_answer": "Incremental (differential) costs and opportunity costs"
    },
    {
        "question": "Absorption costing differs from marginal costing in that it:",
        "options": ["Excludes variable costs from product cost", "Includes fixed production overheads in the cost of each unit produced", "Only applies to service industries", "Ignores direct labour costs"],
        "correct_answer": "Includes fixed production overheads in the cost of each unit produced"
    },
    {
        "question": "The margin of safety represents:",
        "options": ["The minimum selling price to cover costs", "The excess of actual or budgeted sales over the break-even sales level", "The difference between fixed and variable costs", "The maximum level of production capacity"],
        "correct_answer": "The excess of actual or budgeted sales over the break-even sales level"
    },
    {
        "question": "Which of the following is a relevant cost for decision making?",
        "options": ["Depreciation on existing equipment", "Future incremental cash cost", "Allocated head office overhead", "Historical purchase price of materials already bought"],
        "correct_answer": "Future incremental cash cost"
    },
    {
        "question": "Cost-Volume-Profit (CVP) analysis assumes that:",
        "options": ["Costs are non-linear across all output levels", "Selling price, variable cost per unit and fixed costs remain constant within the relevant range", "Fixed costs change proportionally with output", "All production is sold in a different period to when it is made"],
        "correct_answer": "Selling price, variable cost per unit and fixed costs remain constant within the relevant range"
    },
    {
        "question": "Which statement correctly describes a direct cost?",
        "options": ["A cost that cannot be traced to a specific cost object", "A cost that is fixed regardless of output", "A cost that can be directly traced to a specific product, job or department", "An overhead cost shared across departments"],
        "correct_answer": "A cost that can be directly traced to a specific product, job or department"
    },
    {
        "question": "When production exceeds sales in a period, absorption costing will show:",
        "options": ["Lower profit than marginal costing", "The same profit as marginal costing", "Higher profit than marginal costing", "A loss regardless of sales volume"],
        "correct_answer": "Higher profit than marginal costing"
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
        "title": "Diploma in Cost Accounting - Final Assessment",
        "description": "Test your knowledge of cost classification, CVP analysis, marginal costing and decision making. You need 70% to pass.",
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
