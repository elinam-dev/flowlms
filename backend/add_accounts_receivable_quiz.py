import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "173a7bfb-e8c3-47e4-bdb5-91a3e1dc3c47"

QUESTIONS = [
    {
        "question": "Accounts Receivable (AR) represents:",
        "options": ["Money owed by the company to its suppliers", "Money owed to the company by customers for goods or services delivered on credit", "Cash held in the company's bank account", "Long-term loans from financial institutions"],
        "correct_answer": "Money owed to the company by customers for goods or services delivered on credit"
    },
    {
        "question": "The Accounts Receivable process flow typically begins with:",
        "options": ["Collecting payment from the customer", "Issuing a credit note", "Extending credit and raising a sales invoice", "Performing a bank reconciliation"],
        "correct_answer": "Extending credit and raising a sales invoice"
    },
    {
        "question": "A credit policy defines:",
        "options": ["How the company invests surplus cash", "The terms and conditions under which credit is extended to customers, including credit limits and payment terms", "The process for paying suppliers", "The company's borrowing strategy"],
        "correct_answer": "The terms and conditions under which credit is extended to customers, including credit limits and payment terms"
    },
    {
        "question": "Credit risk assessment involves evaluating:",
        "options": ["The company's internal audit procedures", "A customer's ability and willingness to pay based on financial history, creditworthiness and payment behaviour", "The market price of the company's shares", "The depreciation policy for fixed assets"],
        "correct_answer": "A customer's ability and willingness to pay based on financial history, creditworthiness and payment behaviour"
    },
    {
        "question": "Which of the following is a key element of an effective billing and invoicing process?",
        "options": ["Delaying invoice dispatch to manage cash flow", "Issuing accurate, timely invoices with clear payment terms to reduce disputes and delays", "Sending invoices only at year end", "Combining multiple customers' charges on a single invoice"],
        "correct_answer": "Issuing accurate, timely invoices with clear payment terms to reduce disputes and delays"
    },
    {
        "question": "The Debtor Days (Days Sales Outstanding) ratio measures:",
        "options": ["How many days it takes to sell inventory", "The average number of days it takes to collect payment from customers after a sale", "The number of days before supplier invoices are due", "The average credit period offered by suppliers"],
        "correct_answer": "The average number of days it takes to collect payment from customers after a sale"
    },
    {
        "question": "An effective receivables collection strategy would include:",
        "options": ["Ignoring overdue accounts to maintain customer relationships", "Systematic follow-up on overdue invoices, escalation procedures and offering early payment discounts", "Extending credit limits to all customers regardless of risk", "Waiting until year end to chase outstanding balances"],
        "correct_answer": "Systematic follow-up on overdue invoices, escalation procedures and offering early payment discounts"
    },
    {
        "question": "Cash application in accounts receivable refers to:",
        "options": ["Applying for a bank overdraft", "The process of matching incoming customer payments to the correct outstanding invoices", "Transferring funds between company bank accounts", "Calculating the cash discount available to customers"],
        "correct_answer": "The process of matching incoming customer payments to the correct outstanding invoices"
    },
    {
        "question": "The Aged Receivables Report is used to:",
        "options": ["Track supplier payment schedules", "Identify overdue customer balances categorised by how long they have been outstanding", "Prepare the monthly payroll", "Calculate VAT liability"],
        "correct_answer": "Identify overdue customer balances categorised by how long they have been outstanding"
    },
    {
        "question": "Which technology trend is transforming accounts receivable management?",
        "options": ["Manual ledger bookkeeping", "Automation and AI-driven tools for invoice processing, payment matching and collections", "Fax-based invoice delivery", "Paper-based credit applications"],
        "correct_answer": "Automation and AI-driven tools for invoice processing, payment matching and collections"
    },
    {
        "question": "A bad debt provision is created to:",
        "options": ["Increase the reported profit for the period", "Account for the estimated portion of receivables that may not be collected", "Reduce the company's tax liability immediately", "Write off all outstanding customer balances"],
        "correct_answer": "Account for the estimated portion of receivables that may not be collected"
    },
    {
        "question": "Which of the following would reduce the Debtor Days ratio?",
        "options": ["Extending credit terms to all customers", "Improving collections processes and offering early payment incentives", "Increasing the credit limit for high-risk customers", "Delaying the issuance of invoices"],
        "correct_answer": "Improving collections processes and offering early payment incentives"
    },
    {
        "question": "Reconciliation in accounts receivable ensures that:",
        "options": ["All supplier invoices are paid on time", "The AR ledger balance agrees with the general ledger and customer statements", "Payroll is processed accurately", "Fixed assets are correctly depreciated"],
        "correct_answer": "The AR ledger balance agrees with the general ledger and customer statements"
    },
    {
        "question": "A credit note issued to a customer will:",
        "options": ["Increase the amount the customer owes", "Reduce the outstanding balance owed by the customer", "Create a new liability on the company's balance sheet", "Increase the company's revenue"],
        "correct_answer": "Reduce the outstanding balance owed by the customer"
    },
    {
        "question": "Effective accounts receivable management directly impacts:",
        "options": ["Only the company's gross profit margin", "The company's cash flow, working capital and overall financial health", "Only the tax payable at year end", "The company's fixed asset register"],
        "correct_answer": "The company's cash flow, working capital and overall financial health"
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
        "title": "Accounts Receivable Management - Final Assessment",
        "description": "Test your knowledge of AR processes, credit management, collections and reconciliation. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
