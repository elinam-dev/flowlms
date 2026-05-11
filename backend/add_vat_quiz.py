import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "7cc7787d-8050-4432-a5ae-6fc22664fe18"

QUESTIONS = [
    {
        "question": "Value-Added Tax (VAT) is best described as:",
        "options": ["A direct tax on company profits", "An indirect tax levied on the value added at each stage of production and distribution", "A tax on personal income", "A one-time tax paid only by the final consumer"],
        "correct_answer": "An indirect tax levied on the value added at each stage of production and distribution"
    },
    {
        "question": "In the UK, which organisation administers VAT?",
        "options": ["The Bank of England", "The Financial Conduct Authority (FCA)", "HM Revenue and Customs (HMRC)", "Companies House"],
        "correct_answer": "HM Revenue and Customs (HMRC)"
    },
    {
        "question": "The standard rate of VAT in the UK is currently:",
        "options": ["5%", "10%", "15%", "20%"],
        "correct_answer": "20%"
    },
    {
        "question": "A business must register for VAT in the UK when its taxable turnover exceeds:",
        "options": ["The VAT registration threshold set by HMRC", "Any amount of turnover", "Only when it becomes a limited company", "When it employs more than 10 staff"],
        "correct_answer": "The VAT registration threshold set by HMRC"
    },
    {
        "question": "Input VAT refers to:",
        "options": ["VAT charged on sales made by the business", "VAT paid by the business on its purchases and expenses", "The total VAT liability payable to HMRC", "VAT on imported goods only"],
        "correct_answer": "VAT paid by the business on its purchases and expenses"
    },
    {
        "question": "Output VAT refers to:",
        "options": ["VAT reclaimed on business purchases", "VAT charged by the business on its taxable sales", "VAT paid on capital expenditure", "VAT on zero-rated supplies"],
        "correct_answer": "VAT charged by the business on its taxable sales"
    },
    {
        "question": "The VAT liability payable to HMRC is calculated as:",
        "options": ["Input VAT + Output VAT", "Output VAT - Input VAT", "Total Sales x VAT Rate", "Total Purchases x VAT Rate"],
        "correct_answer": "Output VAT - Input VAT"
    },
    {
        "question": "Zero-rated supplies in the UK VAT system means:",
        "options": ["The supply is exempt from VAT and no VAT can be reclaimed", "VAT is charged at 0% but the business can still reclaim input VAT on related costs", "The supply is outside the scope of VAT entirely", "VAT is charged at the reduced rate of 5%"],
        "correct_answer": "VAT is charged at 0% but the business can still reclaim input VAT on related costs"
    },
    {
        "question": "Which of the following is typically a VAT-exempt supply in the UK?",
        "options": ["Standard-rated retail sales", "Financial services and insurance", "Zero-rated food items", "Reduced-rate domestic fuel"],
        "correct_answer": "Financial services and insurance"
    },
    {
        "question": "A VAT invoice must include:",
        "options": ["Only the total amount payable", "The supplier's VAT registration number, a unique invoice number, the VAT rate and the VAT amount charged", "Only the customer's name and address", "The supplier's bank account details only"],
        "correct_answer": "The supplier's VAT registration number, a unique invoice number, the VAT rate and the VAT amount charged"
    },
    {
        "question": "The Finance Act 2021 introduced changes to VAT in the UK that included:",
        "options": ["Abolishing VAT on all food items", "Extending the temporary reduced VAT rate for the hospitality sector and introducing Making Tax Digital (MTD) requirements", "Increasing the standard VAT rate to 25%", "Removing VAT registration requirements for small businesses"],
        "correct_answer": "Extending the temporary reduced VAT rate for the hospitality sector and introducing Making Tax Digital (MTD) requirements"
    },
    {
        "question": "A taxable person for VAT purposes is:",
        "options": ["Any individual who pays income tax", "Any person or business that makes taxable supplies and is registered or required to register for VAT", "Only limited companies with turnover above 1 million", "Only businesses that import goods"],
        "correct_answer": "Any person or business that makes taxable supplies and is registered or required to register for VAT"
    },
    {
        "question": "VAT deregistration is appropriate when:",
        "options": ["A business wants to avoid paying corporation tax", "A business's taxable turnover falls below the deregistration threshold or it ceases to make taxable supplies", "A business changes its trading name", "A business opens a new branch"],
        "correct_answer": "A business's taxable turnover falls below the deregistration threshold or it ceases to make taxable supplies"
    },
    {
        "question": "VAT record-keeping requirements include retaining:",
        "options": ["Only sales invoices for the current year", "VAT invoices, receipts, VAT account records and VAT returns for a minimum of six years", "Only the annual VAT return", "Bank statements only"],
        "correct_answer": "VAT invoices, receipts, VAT account records and VAT returns for a minimum of six years"
    },
    {
        "question": "The reduced VAT rate of 5% in the UK applies to supplies such as:",
        "options": ["Standard retail clothing", "Domestic fuel and power, and certain energy-saving materials", "Business-to-business professional services", "All food and drink items"],
        "correct_answer": "Domestic fuel and power, and certain energy-saving materials"
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
        "title": "Basics of Value-Added Tax - Final Assessment",
        "description": "Test your knowledge of VAT concepts, UK VAT rates, registration, invoicing and record-keeping. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
