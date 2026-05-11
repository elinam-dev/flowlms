import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "1a8b9fb1-d47b-47cd-9569-ce1ce1d313d7"

QUESTIONS = [
    {
        "question": "What is the primary purpose of management accounting?",
        "options": ["To prepare statutory financial statements for external users", "To provide relevant financial and non-financial information to internal managers for decision-making", "To calculate tax liabilities for the business", "To audit the company's financial records"],
        "correct_answer": "To provide relevant financial and non-financial information to internal managers for decision-making"
    },
    {
        "question": "Which of the following best describes a variable cost?",
        "options": ["A cost that remains constant regardless of output level", "A cost that changes in direct proportion to the level of activity", "A cost that is fixed in the short term but variable in the long term", "A cost that is allocated across departments"],
        "correct_answer": "A cost that changes in direct proportion to the level of activity"
    },
    {
        "question": "In the Foodly Inc. case study, marginal costing was applied to determine:",
        "options": ["The total fixed cost allocation per product", "The contribution each product makes towards covering fixed costs and generating profit", "The standard cost per unit of production", "The depreciation charge for the period"],
        "correct_answer": "The contribution each product makes towards covering fixed costs and generating profit"
    },
    {
        "question": "Cost-Volume-Profit (CVP) analysis helps management to:",
        "options": ["Prepare the annual tax return", "Understand the relationship between costs, volume and profit to support planning decisions", "Allocate overhead costs to products using activity drivers", "Record journal entries for cost transactions"],
        "correct_answer": "Understand the relationship between costs, volume and profit to support planning decisions"
    },
    {
        "question": "Which costing system assigns costs to products based on the activities that drive those costs?",
        "options": ["Marginal costing", "Absorption costing", "Activity-Based Costing (ABC)", "Standard costing"],
        "correct_answer": "Activity-Based Costing (ABC)"
    },
    {
        "question": "Job costing is most appropriate for:",
        "options": ["Mass production of identical units", "Unique or customised products and projects where costs are tracked per job", "Service industries with no physical output", "Continuous process manufacturing"],
        "correct_answer": "Unique or customised products and projects where costs are tracked per job"
    },
    {
        "question": "The contribution per unit is calculated as:",
        "options": ["Selling Price - Total Fixed Costs", "Selling Price - Variable Cost per Unit", "Total Revenue - Total Costs", "Gross Profit / Number of Units"],
        "correct_answer": "Selling Price - Variable Cost per Unit"
    },
    {
        "question": "Which of the following is an example of a semi-variable (mixed) cost?",
        "options": ["Factory rent", "Direct materials", "A telephone bill with a fixed line rental plus a variable usage charge", "Straight-line depreciation"],
        "correct_answer": "A telephone bill with a fixed line rental plus a variable usage charge"
    },
    {
        "question": "Process costing is best suited to industries that:",
        "options": ["Produce unique, one-off products", "Manufacture large volumes of homogeneous products through continuous processes", "Provide professional services to clients", "Operate on a project-by-project basis"],
        "correct_answer": "Manufacture large volumes of homogeneous products through continuous processes"
    },
    {
        "question": "When making a short-term decision about whether to accept a special order below normal selling price, management should focus on:",
        "options": ["Total absorption cost per unit", "Whether the order generates a positive contribution", "The historical cost of the product", "The standard overhead rate"],
        "correct_answer": "Whether the order generates a positive contribution"
    },
    {
        "question": "The break-even point is the level of output at which:",
        "options": ["Total revenue equals total variable costs", "Total revenue equals total costs (fixed + variable)", "Contribution equals zero", "Fixed costs are fully recovered and profit begins"],
        "correct_answer": "Total revenue equals total costs (fixed + variable)"
    },
    {
        "question": "Which statement about fixed costs is correct within the relevant range?",
        "options": ["Fixed costs increase proportionally with output", "Fixed costs per unit decrease as output increases", "Fixed costs per unit remain constant at all output levels", "Fixed costs are always controllable by management"],
        "correct_answer": "Fixed costs per unit decrease as output increases"
    },
    {
        "question": "A limiting factor (key factor) in production planning refers to:",
        "options": ["A cost that cannot be reduced", "A scarce resource that constrains the level of activity and output", "A fixed overhead that cannot be avoided", "A variance that exceeds the acceptable threshold"],
        "correct_answer": "A scarce resource that constrains the level of activity and output"
    },
    {
        "question": "When a limiting factor exists, products should be ranked by:",
        "options": ["Highest selling price per unit", "Highest total revenue", "Highest contribution per unit of the limiting factor", "Lowest variable cost per unit"],
        "correct_answer": "Highest contribution per unit of the limiting factor"
    },
    {
        "question": "The lesson summary of this course emphasises that effective strategy execution requires:",
        "options": ["Focusing exclusively on reducing fixed costs", "Aligning cost information with strategic goals to support informed management decisions", "Maximising production volume regardless of demand", "Eliminating all variable costs from the business model"],
        "correct_answer": "Aligning cost information with strategic goals to support informed management decisions"
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
        "title": "Cost and Management Accounting - Final Assessment",
        "description": "Test your knowledge of cost classification, CVP analysis, costing systems and strategic decision-making. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
