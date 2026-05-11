import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "fff9190e-0f7f-483d-b91b-2299013f062c"

QUESTIONS = [
    {
        "question": "What is the correct order of the first three steps in the accounting cycle?",
        "options": ["Post, Journalize, Analyze", "Analyze, Journalize, Post", "Journalize, Analyze, Post", "Post, Analyze, Journalize"],
        "correct_answer": "Analyze, Journalize, Post"
    },
    {
        "question": "The general journal is used to:",
        "options": ["Summarise ledger account balances", "Record the original entry of financial transactions in chronological order", "Prepare the trial balance", "Close temporary accounts at year end"],
        "correct_answer": "Record the original entry of financial transactions in chronological order"
    },
    {
        "question": "Posting in the accounting cycle refers to:",
        "options": ["Preparing adjusting entries", "Transferring journal entries to the appropriate ledger accounts", "Sending invoices to customers", "Preparing the income statement"],
        "correct_answer": "Transferring journal entries to the appropriate ledger accounts"
    },
    {
        "question": "An unadjusted trial balance is prepared to:",
        "options": ["Finalise the financial statements", "Verify that total debits equal total credits before adjustments", "Record closing entries", "Calculate tax payable"],
        "correct_answer": "Verify that total debits equal total credits before adjustments"
    },
    {
        "question": "Adjusting entries are made at the end of a period to:",
        "options": ["Correct errors in the original journal entries only", "Ensure revenues and expenses are recognised in the correct accounting period", "Close all income and expense accounts", "Record cash transactions missed during the period"],
        "correct_answer": "Ensure revenues and expenses are recognised in the correct accounting period"
    },
    {
        "question": "Which financial statement shows a company's revenues and expenses over a period?",
        "options": ["Balance Sheet", "Statement of Cash Flows", "Income Statement", "Statement of Changes in Equity"],
        "correct_answer": "Income Statement"
    },
    {
        "question": "The Balance Sheet reports:",
        "options": ["Revenues and expenses for the period", "Cash inflows and outflows", "Assets, liabilities and equity at a specific point in time", "Changes in retained earnings over the year"],
        "correct_answer": "Assets, liabilities and equity at a specific point in time"
    },
    {
        "question": "Closing entries are used to:",
        "options": ["Open new accounts at the start of the year", "Transfer balances of temporary accounts (revenues, expenses, dividends) to retained earnings", "Prepare the adjusted trial balance", "Record accruals and prepayments"],
        "correct_answer": "Transfer balances of temporary accounts (revenues, expenses, dividends) to retained earnings"
    },
    {
        "question": "Which of the following is a temporary account?",
        "options": ["Accounts Receivable", "Retained Earnings", "Sales Revenue", "Equipment"],
        "correct_answer": "Sales Revenue"
    },
    {
        "question": "The post-closing trial balance contains only:",
        "options": ["Revenue and expense accounts", "Permanent (real) accounts - assets, liabilities and equity", "Temporary accounts with zero balances", "Adjusting entries"],
        "correct_answer": "Permanent (real) accounts - assets, liabilities and equity"
    },
    {
        "question": "A classified balance sheet organises assets into:",
        "options": ["Fixed and intangible assets only", "Current assets and non-current (long-term) assets", "Revenue assets and capital assets", "Tangible and financial assets"],
        "correct_answer": "Current assets and non-current (long-term) assets"
    },
    {
        "question": "The Statement of Owner's Equity shows:",
        "options": ["The company's cash position at year end", "Changes in the owner's capital account during the period", "Total liabilities owed to creditors", "The company's gross profit margin"],
        "correct_answer": "Changes in the owner's capital account during the period"
    },
    {
        "question": "Which accounting concept requires revenues to be matched with the expenses incurred to generate them?",
        "options": ["Going concern concept", "Matching (accruals) concept", "Prudence concept", "Consistency concept"],
        "correct_answer": "Matching (accruals) concept"
    },
    {
        "question": "A single-step income statement presents:",
        "options": ["Gross profit separately from operating expenses", "All revenues together and all expenses together, with one calculation for net income", "Operating income and non-operating income in separate sections", "Only cash-based revenues and expenses"],
        "correct_answer": "All revenues together and all expenses together, with one calculation for net income"
    },
    {
        "question": "Which of the following would appear as a current liability on the balance sheet?",
        "options": ["Long-term bank loan", "Accounts payable", "Equipment", "Retained earnings"],
        "correct_answer": "Accounts payable"
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
        "title": "The Accounting Cycle and Financial Statements - Final Assessment",
        "description": "Test your understanding of the full accounting cycle, from transaction analysis to financial statement preparation. You need 70% to pass.",
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
