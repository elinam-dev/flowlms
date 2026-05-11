import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "30aa996f-32d1-49f9-9829-616d157ea438"

QUESTIONS = [
    {
        "question": "Business accounting is primarily used to:",
        "options": ["Manage employee performance reviews", "Record, summarise and communicate a business's financial transactions to support decision-making", "Set product prices based on market demand", "Manage the company's marketing budget"],
        "correct_answer": "Record, summarise and communicate a business's financial transactions to support decision-making"
    },
    {
        "question": "Which of the following is the correct accounting equation?",
        "options": ["Assets = Revenue - Expenses", "Assets = Liabilities + Equity", "Profit = Assets - Liabilities", "Equity = Assets + Liabilities"],
        "correct_answer": "Assets = Liabilities + Equity"
    },
    {
        "question": "In double-entry bookkeeping, every transaction requires:",
        "options": ["A single entry in the cash book", "At least two entries — a debit in one account and a credit in another", "An entry only when cash is involved", "Approval from an external auditor"],
        "correct_answer": "At least two entries — a debit in one account and a credit in another"
    },
    {
        "question": "Which financial statement reports a business's revenues and expenses over a specific period?",
        "options": ["Balance Sheet", "Statement of Cash Flows", "Income Statement (Profit and Loss Account)", "Statement of Changes in Equity"],
        "correct_answer": "Income Statement (Profit and Loss Account)"
    },
    {
        "question": "The Balance Sheet shows:",
        "options": ["Revenue earned and expenses incurred during the year", "Cash inflows and outflows from operating, investing and financing activities", "The financial position of a business at a specific point in time", "The budget versus actual performance for the period"],
        "correct_answer": "The financial position of a business at a specific point in time"
    },
    {
        "question": "Gross profit is calculated as:",
        "options": ["Revenue - All Operating Expenses", "Revenue - Cost of Goods Sold", "Net Profit + Tax", "Operating Profit + Depreciation"],
        "correct_answer": "Revenue - Cost of Goods Sold"
    },
    {
        "question": "Which of the following is classified as a current liability?",
        "options": ["Long-term bank loan", "Motor vehicles", "Trade payables (creditors)", "Retained earnings"],
        "correct_answer": "Trade payables (creditors)"
    },
    {
        "question": "Retained earnings represent:",
        "options": ["Cash held in the company's bank account", "Cumulative profits kept in the business after dividends have been paid", "The original capital invested by shareholders", "Short-term borrowings from the bank"],
        "correct_answer": "Cumulative profits kept in the business after dividends have been paid"
    },
    {
        "question": "The accruals concept in business accounting means:",
        "options": ["Transactions are only recorded when cash is received or paid", "Revenue and expenses are recognised in the period they are earned or incurred, regardless of cash movement", "All assets are recorded at their current market value", "Profits are only recognised at year end"],
        "correct_answer": "Revenue and expenses are recognised in the period they are earned or incurred, regardless of cash movement"
    },
    {
        "question": "A Trial Balance is prepared to:",
        "options": ["Calculate the company's tax liability", "Verify that total debits equal total credits in the ledger before preparing financial statements", "Show the company's cash position at year end", "List all outstanding customer invoices"],
        "correct_answer": "Verify that total debits equal total credits in the ledger before preparing financial statements"
    },
    {
        "question": "Depreciation is charged on fixed assets in order to:",
        "options": ["Increase the asset's value on the balance sheet", "Allocate the cost of the asset systematically over its useful life", "Set aside cash for future asset replacement", "Reduce the company's VAT liability"],
        "correct_answer": "Allocate the cost of the asset systematically over its useful life"
    },
    {
        "question": "Which of the following best describes a sole trader business structure?",
        "options": ["A business owned by shareholders with limited liability", "A business owned and operated by one individual who has unlimited personal liability", "A partnership between two or more companies", "A government-owned enterprise"],
        "correct_answer": "A business owned and operated by one individual who has unlimited personal liability"
    },
    {
        "question": "Cash flow from operating activities includes:",
        "options": ["Purchase of new machinery", "Repayment of long-term loans", "Cash received from customers and cash paid to suppliers and employees", "Proceeds from issuing new shares"],
        "correct_answer": "Cash received from customers and cash paid to suppliers and employees"
    },
    {
        "question": "Working capital is calculated as:",
        "options": ["Total Assets - Total Liabilities", "Current Assets - Current Liabilities", "Fixed Assets - Long-term Debt", "Equity - Retained Earnings"],
        "correct_answer": "Current Assets - Current Liabilities"
    },
    {
        "question": "Which accounting concept states that a business should be treated as separate from its owners for accounting purposes?",
        "options": ["Going concern concept", "Matching concept", "Business entity concept", "Prudence concept"],
        "correct_answer": "Business entity concept"
    },
    {
        "question": "An invoice issued to a customer creates which entry in the business's books?",
        "options": ["A debit to accounts payable and a credit to sales", "A debit to accounts receivable and a credit to sales revenue", "A debit to cash and a credit to accounts receivable", "A debit to expenses and a credit to cash"],
        "correct_answer": "A debit to accounts receivable and a credit to sales revenue"
    },
    {
        "question": "The purpose of a bank reconciliation statement is to:",
        "options": ["Prepare the annual tax return", "Ensure the cash book balance agrees with the bank statement balance by identifying and explaining differences", "Calculate the company's net profit for the period", "Verify that all supplier invoices have been paid"],
        "correct_answer": "Ensure the cash book balance agrees with the bank statement balance by identifying and explaining differences"
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
        "title": "Introduction to Business Accounting - Final Assessment",
        "description": "Test your understanding of core business accounting principles, financial statements, double-entry bookkeeping and working capital. You need 70% to pass.",
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
