import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "3cf997a2-b127-4db7-a442-0febc3f2d51e"

QUESTIONS = [
    {
        "question": "Which government body is responsible for collecting taxes in the United Kingdom?",
        "options": ["The Bank of England", "HM Revenue and Customs (HMRC)", "The Financial Conduct Authority (FCA)", "The Treasury Select Committee"],
        "correct_answer": "HM Revenue and Customs (HMRC)"
    },
    {
        "question": "A Self-Assessment Tax Return in the UK must typically be submitted online by:",
        "options": ["31 October each year", "31 January following the end of the tax year", "5 April each year", "30 June each year"],
        "correct_answer": "31 January following the end of the tax year"
    },
    {
        "question": "National Insurance Contributions (NICs) in the UK are paid by:",
        "options": ["Employers only", "Employees only", "Both employers and employees", "Self-employed individuals only"],
        "correct_answer": "Both employers and employees"
    },
    {
        "question": "Income Tax in the UK is charged on:",
        "options": ["Only employment income", "Only investment income", "All taxable income including employment, self-employment, rental and savings income", "Company profits only"],
        "correct_answer": "All taxable income including employment, self-employment, rental and savings income"
    },
    {
        "question": "PAYE (Pay As You Earn) is a system used to:",
        "options": ["File annual self-assessment returns", "Collect income tax and NICs directly from employees' wages by employers", "Calculate corporation tax", "Register businesses for VAT"],
        "correct_answer": "Collect income tax and NICs directly from employees' wages by employers"
    },
    {
        "question": "Capital Gains Tax (CGT) is charged on:",
        "options": ["Regular employment income", "Profits made from selling or disposing of assets that have increased in value", "Company dividends only", "Inherited property regardless of gain"],
        "correct_answer": "Profits made from selling or disposing of assets that have increased in value"
    },
    {
        "question": "Value Added Tax (VAT) is best described as:",
        "options": ["A direct tax on company profits", "An indirect tax charged on the sale of goods and services at each stage of production", "A tax on personal income", "A tax on capital gains"],
        "correct_answer": "An indirect tax charged on the sale of goods and services at each stage of production"
    },
    {
        "question": "Corporation Tax in the UK is levied on:",
        "options": ["Personal income of company directors", "Profits earned by limited companies and other corporate entities", "Dividends paid to shareholders only", "Capital gains of individuals"],
        "correct_answer": "Profits earned by limited companies and other corporate entities"
    },
    {
        "question": "Inheritance Tax (IHT) in the UK is generally charged on:",
        "options": ["All gifts made during a person's lifetime", "The estate of a deceased person above the nil-rate band threshold", "Income received from investments", "Business profits above a set threshold"],
        "correct_answer": "The estate of a deceased person above the nil-rate band threshold"
    },
    {
        "question": "Trading income for tax purposes refers to:",
        "options": ["Income from employment only", "Profits arising from a trade, profession or vocation carried on by an individual or business", "Rental income from property", "Dividends received from shares"],
        "correct_answer": "Profits arising from a trade, profession or vocation carried on by an individual or business"
    },
    {
        "question": "Double-entry accounting requires that every transaction:",
        "options": ["Is recorded once in the cash book", "Has equal and opposite debit and credit entries", "Is approved by a tax authority", "Is recorded only when cash is received or paid"],
        "correct_answer": "Has equal and opposite debit and credit entries"
    },
    {
        "question": "Which of the following is an example of a direct tax?",
        "options": ["Value Added Tax (VAT)", "Excise duty on fuel", "Income Tax", "Customs duty on imports"],
        "correct_answer": "Income Tax"
    },
    {
        "question": "Import and export taxes are primarily administered to:",
        "options": ["Regulate domestic income tax rates", "Control the flow of goods across borders and generate government revenue", "Replace VAT on international transactions", "Determine corporation tax rates"],
        "correct_answer": "Control the flow of goods across borders and generate government revenue"
    },
    {
        "question": "Management accounting differs from financial accounting in that it:",
        "options": ["Is mandatory and regulated by law", "Focuses on providing internal information to help managers make decisions", "Only deals with tax calculations", "Produces reports exclusively for shareholders"],
        "correct_answer": "Focuses on providing internal information to help managers make decisions"
    },
    {
        "question": "A tax accountant's primary role includes:",
        "options": ["Setting government tax policy", "Ensuring clients comply with tax laws, minimise tax liabilities legally and file accurate returns", "Auditing company financial statements", "Managing company payroll systems"],
        "correct_answer": "Ensuring clients comply with tax laws, minimise tax liabilities legally and file accurate returns"
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
        "title": "Tax Accounting Systems and Administration - Final Assessment",
        "description": "Test your knowledge of UK tax systems including income tax, VAT, corporation tax and self-assessment. You need 70% to pass.",
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
