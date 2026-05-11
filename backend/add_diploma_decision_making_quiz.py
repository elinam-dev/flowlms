import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "c1fae7e5-41fe-4ab5-b6a2-61d759ecfa43"

QUESTIONS = [
    {
        "question": "The accounting equation states that:",
        "options": ["Assets = Liabilities - Equity", "Assets = Liabilities + Equity", "Equity = Assets + Liabilities", "Liabilities = Assets + Equity"],
        "correct_answer": "Assets = Liabilities + Equity"
    },
    {
        "question": "A Balance Sheet provides a snapshot of a company's financial position:",
        "options": ["Over a full financial year", "At a specific point in time", "For the previous five years", "Based on projected future values"],
        "correct_answer": "At a specific point in time"
    },
    {
        "question": "Depreciation in accounting represents:",
        "options": ["The market value decline of an asset", "The systematic allocation of an asset's cost over its useful life", "Cash set aside to replace assets", "The interest charged on borrowed funds"],
        "correct_answer": "The systematic allocation of an asset's cost over its useful life"
    },
    {
        "question": "The conservatism (prudence) concept in accounting requires that:",
        "options": ["Profits are recognised as early as possible", "Losses and liabilities are recognised as soon as they are probable, while gains are only recognised when certain", "All assets are recorded at market value", "Revenue is always deferred to the next period"],
        "correct_answer": "Losses and liabilities are recognised as soon as they are probable, while gains are only recognised when certain"
    },
    {
        "question": "Preference shares differ from ordinary shares in that they:",
        "options": ["Always carry voting rights", "Receive a fixed dividend before ordinary shareholders are paid", "Represent debt on the balance sheet", "Are only issued by government entities"],
        "correct_answer": "Receive a fixed dividend before ordinary shareholders are paid"
    },
    {
        "question": "Which of the following best describes the concept of value in financial accounting?",
        "options": ["Value is always equal to the original purchase price", "Value can be measured as historical cost, fair value or net realisable value depending on the context", "Value is determined solely by market share price", "Value only applies to tangible assets"],
        "correct_answer": "Value can be measured as historical cost, fair value or net realisable value depending on the context"
    },
    {
        "question": "In a double-entry bookkeeping system, every transaction affects:",
        "options": ["Only one account", "At least two accounts with equal debits and credits", "The cash account and one other account only", "The income statement only"],
        "correct_answer": "At least two accounts with equal debits and credits"
    },
    {
        "question": "The Investor's Formula in financial decision-making focuses on:",
        "options": ["Minimising tax liabilities", "Evaluating return relative to risk to determine investment value", "Maximising short-term cash flow", "Reducing the company's debt-to-equity ratio"],
        "correct_answer": "Evaluating return relative to risk to determine investment value"
    },
    {
        "question": "Expenditure is classified as capital expenditure when:",
        "options": ["It is incurred on a recurring basis for day-to-day operations", "It provides a benefit beyond the current accounting period and is recorded as an asset", "It is paid in cash immediately", "It relates to employee salaries"],
        "correct_answer": "It provides a benefit beyond the current accounting period and is recorded as an asset"
    },
    {
        "question": "Market-related concepts in financial accounting include:",
        "options": ["Standard costing and variance analysis", "Market capitalisation, earnings yield and dividend yield", "Budgetary control and cash flow forecasting", "Depreciation methods and asset revaluation"],
        "correct_answer": "Market capitalisation, earnings yield and dividend yield"
    },
    {
        "question": "When analysing a company's balance sheet for decision-making, which section reveals the company's obligations to external parties?",
        "options": ["Equity section", "Liabilities section", "Non-current assets section", "Revenue reserves"],
        "correct_answer": "Liabilities section"
    },
    {
        "question": "A company issues new ordinary shares. The effect on the balance sheet is:",
        "options": ["Assets decrease and equity decreases", "Assets increase and equity increases", "Liabilities increase and equity decreases", "Assets decrease and liabilities increase"],
        "correct_answer": "Assets increase and equity increases"
    },
    {
        "question": "Which financial statement is most useful for assessing a company's ability to generate cash?",
        "options": ["Balance Sheet", "Income Statement", "Statement of Cash Flows", "Statement of Changes in Equity"],
        "correct_answer": "Statement of Cash Flows"
    },
    {
        "question": "The concept of 'going concern' assumes that:",
        "options": ["The business will be liquidated in the near future", "The business will continue to operate for the foreseeable future", "All assets will be sold at market value", "The company has no outstanding liabilities"],
        "correct_answer": "The business will continue to operate for the foreseeable future"
    },
    {
        "question": "Inner workings of companies relevant to shareholders include:",
        "options": ["Only the company's tax filings", "Dividend policy, retained earnings, share buybacks and rights issues", "The personal finances of directors", "Only the gross profit margin"],
        "correct_answer": "Dividend policy, retained earnings, share buybacks and rights issues"
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
        "title": "Diploma in Decision Making Using Financial Accounting - Final Assessment",
        "description": "Test your understanding of financial accounting concepts applied to business decision-making. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
