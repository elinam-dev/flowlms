import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Accounting is best defined as:",
        "options": ["The process of managing a company's employees", "The systematic process of recording, classifying, summarising and communicating financial information", "The calculation of tax liabilities only", "The management of a company's physical assets"],
        "correct_answer": "The systematic process of recording, classifying, summarising and communicating financial information"
    },
    {
        "question": "The two main streams of accounting are:",
        "options": ["Tax accounting and audit accounting", "Financial accounting and management accounting", "Cost accounting and payroll accounting", "Bookkeeping and financial planning"],
        "correct_answer": "Financial accounting and management accounting"
    },
    {
        "question": "Which of the following is a basic business model concept in accounting?",
        "options": ["A business acquires resources, uses them to create value and generates revenue", "A business only records transactions when cash is received", "A business reports only to its shareholders", "A business measures success only by headcount"],
        "correct_answer": "A business acquires resources, uses them to create value and generates revenue"
    },
    {
        "question": "On a balance sheet, assets are funded by:",
        "options": ["Revenue and expenses only", "Liabilities and equity", "Cash flows from operations", "Depreciation and amortisation"],
        "correct_answer": "Liabilities and equity"
    },
    {
        "question": "Current liabilities are obligations that must be settled within:",
        "options": ["Five years", "Three years", "One year", "Ten years"],
        "correct_answer": "One year"
    },
    {
        "question": "Non-current assets are assets that:",
        "options": ["Will be converted to cash within 12 months", "Are held for long-term use in the business beyond one year", "Are only intangible in nature", "Are always depreciated over 5 years"],
        "correct_answer": "Are held for long-term use in the business beyond one year"
    },
    {
        "question": "Depreciation is charged on fixed assets to:",
        "options": ["Increase the asset's value over time", "Systematically allocate the cost of the asset over its useful economic life", "Set aside cash for asset replacement", "Reduce the company's tax liability immediately"],
        "correct_answer": "Systematically allocate the cost of the asset over its useful economic life"
    },
    {
        "question": "The Profit and Loss Account (Income Statement) is used to determine:",
        "options": ["The company's total assets at year end", "Whether the company made a profit or loss during the accounting period", "The cash balance at the end of the period", "The total equity of the company"],
        "correct_answer": "Whether the company made a profit or loss during the accounting period"
    },
    {
        "question": "Which of the following is an example of a current asset?",
        "options": ["Land and buildings", "Long-term investments", "Trade receivables (debtors)", "Goodwill"],
        "correct_answer": "Trade receivables (debtors)"
    },
    {
        "question": "The going concern concept assumes that:",
        "options": ["The business will be wound up at the end of the financial year", "The business will continue to operate for the foreseeable future", "All assets will be sold at market value", "The business has no outstanding debts"],
        "correct_answer": "The business will continue to operate for the foreseeable future"
    },
    {
        "question": "Owner's equity increases when:",
        "options": ["The business takes on more debt", "The business makes a profit or the owner injects additional capital", "Assets are sold at a loss", "Liabilities increase"],
        "correct_answer": "The business makes a profit or the owner injects additional capital"
    },
    {
        "question": "A contingent liability should be disclosed in financial statements when:",
        "options": ["It is certain to occur and the amount is known", "It is possible but not probable, or probable but cannot be reliably measured", "It has already been paid", "It relates to a capital expenditure project"],
        "correct_answer": "It is possible but not probable, or probable but cannot be reliably measured"
    },
    {
        "question": "The accruals (matching) concept requires that:",
        "options": ["All transactions are recorded when cash changes hands", "Revenues and expenses are matched to the period in which they are earned or incurred", "Only confirmed transactions are recorded", "Expenses are deferred until the next accounting period"],
        "correct_answer": "Revenues and expenses are matched to the period in which they are earned or incurred"
    },
    {
        "question": "Which financial statement shows the company's financial position at a specific date?",
        "options": ["Income Statement", "Statement of Cash Flows", "Balance Sheet", "Statement of Changes in Equity"],
        "correct_answer": "Balance Sheet"
    },
    {
        "question": "The fundamental accounting equation is:",
        "options": ["Revenue - Expenses = Profit", "Assets = Liabilities + Equity", "Cash = Assets - Liabilities", "Equity = Revenue - Costs"],
        "correct_answer": "Assets = Liabilities + Equity"
    },
    {
        "question": "Provisions in accounting are created for:",
        "options": ["Future capital investments", "Known liabilities of uncertain amount or timing that are probable and can be estimated", "Dividends to be paid next year", "Prepaid expenses carried forward"],
        "correct_answer": "Known liabilities of uncertain amount or timing that are probable and can be estimated"
    },
    {
        "question": "Which of the following best describes the prudence (conservatism) concept?",
        "options": ["Record all anticipated profits immediately", "Recognise losses and liabilities as soon as they are probable, but only recognise gains when they are certain", "Always use the highest possible asset values", "Defer all expenses to future periods"],
        "correct_answer": "Recognise losses and liabilities as soon as they are probable, but only recognise gains when they are certain"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "fundamentals.*accounting", "$options": "i"}})
    if not course:
        print("Course not found")
        return
    print(f"Found: {course['title']}")
    module = await db.modules.find_one({"course_id": course["id"]})
    existing = await db.quizzes.find_one({"module_id": module["id"]})
    if existing:
        await db.quizzes.delete_one({"module_id": module["id"]})
        print("Removed existing quiz")
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module["id"],
        "course_id": course["id"],
        "title": "Fundamentals of Accounting - Final Assessment",
        "description": "Test your understanding of core accounting principles, financial statements, assets, liabilities and equity. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
