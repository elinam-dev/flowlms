import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "c73a35db-27c1-47f0-871e-7993855f24d1"

QUESTIONS = [
    {
        "question": "What is the first step when setting up Sage One for a new business?",
        "options": ["Enter supplier invoices", "Download Sage and create a company account", "Run a bank reconciliation", "Generate a profit and loss report"],
        "correct_answer": "Download Sage and create a company account"
    },
    {
        "question": "In Sage One, the Chart of Accounts is used to:",
        "options": ["List all customers and suppliers", "Organise and categorise all financial transactions by account type", "Record bank statements", "Generate payroll reports"],
        "correct_answer": "Organise and categorise all financial transactions by account type"
    },
    {
        "question": "When you issue a sales invoice in Sage One, it records:",
        "options": ["A payment received from a customer", "An amount owed to you by a customer (accounts receivable)", "A purchase made from a supplier", "A bank transfer between accounts"],
        "correct_answer": "An amount owed to you by a customer (accounts receivable)"
    },
    {
        "question": "A credit note in Sage One is typically raised to:",
        "options": ["Record a new customer payment", "Reverse or reduce a previously issued invoice", "Add a new supplier to the system", "Record a cash purchase"],
        "correct_answer": "Reverse or reduce a previously issued invoice"
    },
    {
        "question": "Bank reconciliation in Sage One involves:",
        "options": ["Matching transactions in Sage with your actual bank statement to ensure they agree", "Paying all outstanding supplier invoices", "Generating a VAT return", "Creating new customer accounts"],
        "correct_answer": "Matching transactions in Sage with your actual bank statement to ensure they agree"
    },
    {
        "question": "When recording a customer receipt in Sage One, you are:",
        "options": ["Creating a new sales invoice", "Allocating a payment received against an outstanding customer invoice", "Entering a supplier credit note", "Posting a journal entry for depreciation"],
        "correct_answer": "Allocating a payment received against an outstanding customer invoice"
    },
    {
        "question": "Which Sage One feature allows you to send invoices directly to customers?",
        "options": ["Bank reconciliation module", "Printing and mailing invoices function", "Chart of accounts editor", "Payroll module"],
        "correct_answer": "Printing and mailing invoices function"
    },
    {
        "question": "A non-invoiced payment in Sage One is used for:",
        "options": ["Recording sales to credit customers", "Posting payments that do not relate to a specific supplier invoice, such as bank charges", "Generating customer statements", "Reconciling VAT returns"],
        "correct_answer": "Posting payments that do not relate to a specific supplier invoice, such as bank charges"
    },
    {
        "question": "Paying a supplier in Sage One will:",
        "options": ["Increase the accounts payable balance", "Reduce the outstanding amount owed to that supplier", "Create a new purchase invoice", "Increase the bank balance"],
        "correct_answer": "Reduce the outstanding amount owed to that supplier"
    },
    {
        "question": "Which report in Sage One shows all money received from customers over a period?",
        "options": ["Aged Creditors Report", "Profit and Loss Statement", "Money Received / Customer Receipts Report", "Trial Balance"],
        "correct_answer": "Money Received / Customer Receipts Report"
    },
    {
        "question": "If you make an error on a posted invoice in Sage One, the correct approach is to:",
        "options": ["Delete the entire company data and start again", "Use the correct invoice entry function to amend or reverse the transaction", "Ignore the error as it cannot be changed", "Manually adjust the bank balance"],
        "correct_answer": "Use the correct invoice entry function to amend or reverse the transaction"
    },
    {
        "question": "The Aged Creditors report in Sage One shows:",
        "options": ["How much customers owe you, broken down by age", "How much you owe suppliers, broken down by age of invoice", "Your bank balance over time", "Monthly sales figures"],
        "correct_answer": "How much you owe suppliers, broken down by age of invoice"
    },
    {
        "question": "Which of the following is a key benefit of using Sage One for bookkeeping?",
        "options": ["It eliminates the need for any financial records", "It automates and organises financial data, reducing manual errors and saving time", "It replaces the need for an accountant entirely", "It only works for large corporations"],
        "correct_answer": "It automates and organises financial data, reducing manual errors and saving time"
    },
    {
        "question": "Cash transactions in Sage One refer to:",
        "options": ["Only transactions made by bank transfer", "Transactions paid or received immediately without a credit period", "Transactions recorded at year end only", "Transactions involving foreign currency"],
        "correct_answer": "Transactions paid or received immediately without a credit period"
    },
    {
        "question": "When generating reports in Sage One, the Profit and Loss report shows:",
        "options": ["The company's assets and liabilities at a point in time", "Income earned and expenses incurred over a specific period", "Outstanding customer invoices only", "Bank reconciliation differences"],
        "correct_answer": "Income earned and expenses incurred over a specific period"
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
        "title": "Sage One Bookkeeping and Accounting - Final Assessment",
        "description": "Test your practical knowledge of Sage One including invoicing, bank reconciliation and reporting. You need 70% to pass.",
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
