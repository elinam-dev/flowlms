import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "b1a49e34-d936-411e-a7f4-7fafde72a56c"

QUESTIONS = [
    {
        "question": "Accounts Payable (AP) represents:",
        "options": ["Money owed to the company by customers", "Money the company owes to suppliers for goods or services received on credit", "Cash held in reserve for capital expenditure", "Long-term bonds issued by the company"],
        "correct_answer": "Money the company owes to suppliers for goods or services received on credit"
    },
    {
        "question": "Which of the following is a key benefit of an efficient accounts payable process?",
        "options": ["Delaying all supplier payments to maximise cash retention", "Maintaining strong supplier relationships, avoiding late payment penalties and optimising cash flow", "Reducing the number of suppliers to one", "Eliminating the need for purchase orders"],
        "correct_answer": "Maintaining strong supplier relationships, avoiding late payment penalties and optimising cash flow"
    },
    {
        "question": "Three-way matching in invoice verification involves matching:",
        "options": ["Three invoices from the same supplier", "The purchase order, goods received note and supplier invoice", "The invoice, payment and bank statement", "The budget, actual spend and forecast"],
        "correct_answer": "The purchase order, goods received note and supplier invoice"
    },
    {
        "question": "When a discrepancy is found between a supplier invoice and the purchase order, the correct action is to:",
        "options": ["Pay the invoice immediately to avoid late fees", "Investigate and resolve the discrepancy with the supplier before authorising payment", "Reject the supplier permanently", "Ignore it if the amount is small"],
        "correct_answer": "Investigate and resolve the discrepancy with the supplier before authorising payment"
    },
    {
        "question": "Payment authorisation in AP ensures that:",
        "options": ["All payments are made on the same day", "Only approved individuals can authorise payments, reducing the risk of fraud and errors", "Suppliers are paid before invoices are verified", "Payments are made without a purchase order"],
        "correct_answer": "Only approved individuals can authorise payments, reducing the risk of fraud and errors"
    },
    {
        "question": "Which of the following is a common fraud risk in accounts payable?",
        "options": ["Paying invoices early to take advantage of discounts", "Duplicate invoice payments, fictitious vendor fraud and unauthorised payments", "Maintaining a vendor master file", "Performing regular supplier statement reconciliations"],
        "correct_answer": "Duplicate invoice payments, fictitious vendor fraud and unauthorised payments"
    },
    {
        "question": "Vendor management in AP involves:",
        "options": ["Only negotiating lower prices with suppliers", "Maintaining accurate vendor records, evaluating performance and building strategic supplier relationships", "Paying all vendors on the same payment terms", "Reducing the vendor base to a single preferred supplier"],
        "correct_answer": "Maintaining accurate vendor records, evaluating performance and building strategic supplier relationships"
    },
    {
        "question": "Vendor performance evaluation typically assesses:",
        "options": ["The vendor's share price and market capitalisation", "Delivery reliability, quality of goods/services, pricing competitiveness and responsiveness", "The vendor's internal HR policies", "Only the vendor's payment terms"],
        "correct_answer": "Delivery reliability, quality of goods/services, pricing competitiveness and responsiveness"
    },
    {
        "question": "Expense auditing in AP is conducted to:",
        "options": ["Increase the number of approved vendors", "Verify that expenses are legitimate, properly authorised and correctly recorded", "Delay payment to suppliers", "Reduce the accounts payable balance artificially"],
        "correct_answer": "Verify that expenses are legitimate, properly authorised and correctly recorded"
    },
    {
        "question": "The month-end closing process in AP includes:",
        "options": ["Issuing new purchase orders for the next month", "Reconciling the AP ledger, accruing for uninvoiced goods received and preparing AP reports", "Paying all outstanding invoices regardless of due date", "Deleting old vendor records"],
        "correct_answer": "Reconciling the AP ledger, accruing for uninvoiced goods received and preparing AP reports"
    },
    {
        "question": "The Creditor Days ratio measures:",
        "options": ["How quickly the company collects money from customers", "The average number of days the company takes to pay its suppliers", "The number of days inventory is held before sale", "The company's cash conversion cycle"],
        "correct_answer": "The average number of days the company takes to pay its suppliers"
    },
    {
        "question": "An AP automation system primarily helps organisations to:",
        "options": ["Manually process each invoice for greater accuracy", "Streamline invoice processing, reduce errors, speed up approvals and improve visibility", "Increase the number of paper-based transactions", "Replace the need for financial controls"],
        "correct_answer": "Streamline invoice processing, reduce errors, speed up approvals and improve visibility"
    },
    {
        "question": "A supplier statement reconciliation is performed to:",
        "options": ["Confirm the company's bank balance", "Ensure the balance on the supplier's statement agrees with the company's AP ledger", "Calculate the VAT owed to HMRC", "Prepare the annual budget"],
        "correct_answer": "Ensure the balance on the supplier's statement agrees with the company's AP ledger"
    },
    {
        "question": "Which internal control best reduces the risk of duplicate payments in AP?",
        "options": ["Paying all invoices on receipt without review", "Implementing a system that flags duplicate invoice numbers, amounts and vendor details before payment", "Allowing any employee to authorise payments", "Maintaining only one bank account for all payments"],
        "correct_answer": "Implementing a system that flags duplicate invoice numbers, amounts and vendor details before payment"
    },
    {
        "question": "AP reports are used by management to:",
        "options": ["Prepare marketing campaigns", "Monitor outstanding liabilities, cash flow requirements and supplier payment performance", "Calculate employee bonuses", "Determine the company's share price"],
        "correct_answer": "Monitor outstanding liabilities, cash flow requirements and supplier payment performance"
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
        "title": "Accounts Payable Management - Final Assessment",
        "description": "Test your knowledge of AP processes, invoice verification, fraud prevention, vendor management and financial controls. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
