import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Financial accounting is primarily concerned with:",
        "options": ["Providing internal cost data to management", "Preparing financial statements for external stakeholders such as investors, creditors and regulators", "Setting product prices and budgets", "Managing day-to-day cash transactions"],
        "correct_answer": "Preparing financial statements for external stakeholders such as investors, creditors and regulators"
    },
    {
        "question": "The three main financial statements produced in financial accounting are:",
        "options": ["Budget, Forecast and Variance Report", "Income Statement, Balance Sheet and Statement of Cash Flows", "Trial Balance, Ledger and Journal", "Cost Report, Profit Plan and Tax Return"],
        "correct_answer": "Income Statement, Balance Sheet and Statement of Cash Flows"
    },
    {
        "question": "Non-current liabilities on a balance sheet represent:",
        "options": ["Amounts owed to suppliers within 12 months", "Obligations due beyond one year such as long-term loans and bonds", "Cash and short-term investments", "Retained earnings from prior years"],
        "correct_answer": "Obligations due beyond one year such as long-term loans and bonds"
    },
    {
        "question": "Current assets are defined as assets that are expected to be converted to cash or used within:",
        "options": ["Five years", "Three years", "One year or the normal operating cycle", "The life of the business"],
        "correct_answer": "One year or the normal operating cycle"
    },
    {
        "question": "Fixed assets (non-current assets) are recorded on the balance sheet at:",
        "options": ["Their current market value", "Their original cost less accumulated depreciation (net book value)", "Their replacement cost", "The amount they could be sold for today"],
        "correct_answer": "Their original cost less accumulated depreciation (net book value)"
    },
    {
        "question": "A provision in financial accounting is created for:",
        "options": ["Future capital expenditure plans", "A liability of uncertain timing or amount that is probable and can be reliably estimated", "Dividends declared but not yet paid", "Prepaid expenses carried forward"],
        "correct_answer": "A liability of uncertain timing or amount that is probable and can be reliably estimated"
    },
    {
        "question": "A contingent liability is:",
        "options": ["A confirmed debt that must be paid immediately", "A possible obligation that depends on the outcome of a future uncertain event", "A fixed overhead allocated to products", "An asset that may be realised in the future"],
        "correct_answer": "A possible obligation that depends on the outcome of a future uncertain event"
    },
    {
        "question": "Owner's funds (equity) on the balance sheet consists of:",
        "options": ["Only the initial capital invested by the owner", "Share capital, retained earnings and other reserves", "Total assets minus current liabilities only", "Long-term debt and preference shares"],
        "correct_answer": "Share capital, retained earnings and other reserves"
    },
    {
        "question": "The balance sheet equation is:",
        "options": ["Assets = Revenue - Expenses", "Assets = Liabilities + Equity", "Equity = Assets + Liabilities", "Revenue = Assets - Liabilities"],
        "correct_answer": "Assets = Liabilities + Equity"
    },
    {
        "question": "The Profit and Loss Account (Income Statement) shows:",
        "options": ["The company's assets and liabilities at year end", "Revenue earned and expenses incurred during the accounting period, resulting in net profit or loss", "Cash received and paid during the period", "Changes in the company's equity over time"],
        "correct_answer": "Revenue earned and expenses incurred during the accounting period, resulting in net profit or loss"
    },
    {
        "question": "Under the Companies Act format, the Profit and Loss Account headings include:",
        "options": ["Only turnover and net profit", "Turnover, cost of sales, gross profit, distribution costs, administrative expenses and operating profit", "Only operating expenses and tax", "Capital expenditure and depreciation only"],
        "correct_answer": "Turnover, cost of sales, gross profit, distribution costs, administrative expenses and operating profit"
    },
    {
        "question": "Intangible assets on a balance sheet include:",
        "options": ["Land and buildings", "Goodwill, patents, trademarks and brand value", "Cash and bank balances", "Trade receivables"],
        "correct_answer": "Goodwill, patents, trademarks and brand value"
    },
    {
        "question": "The effective tax rate is calculated as:",
        "options": ["Tax Expense / Gross Profit x 100", "Tax Expense / Profit Before Tax x 100", "Net Profit / Total Revenue x 100", "Total Tax Paid / Total Assets x 100"],
        "correct_answer": "Tax Expense / Profit Before Tax x 100"
    },
    {
        "question": "Return on Capital Employed (ROCE) measures:",
        "options": ["The dividend yield for shareholders", "How efficiently a company generates profit from its total capital employed", "The ratio of debt to equity", "The gross profit as a percentage of sales"],
        "correct_answer": "How efficiently a company generates profit from its total capital employed"
    },
    {
        "question": "Which of the following best describes the accruals concept in financial accounting?",
        "options": ["Revenue and expenses are recorded only when cash is received or paid", "Revenue is recognised when earned and expenses are recognised when incurred, regardless of cash flow timing", "All transactions are recorded at their historical cost", "Financial statements are prepared on a going concern basis"],
        "correct_answer": "Revenue is recognised when earned and expenses are recognised when incurred, regardless of cash flow timing"
    },
    {
        "question": "Ratio analysis of companies like TCS and RIL is used to:",
        "options": ["Determine the exact share price of the company", "Compare financial performance across periods and against peers to support investment and management decisions", "Calculate the exact tax liability of the company", "Prepare the company's annual budget"],
        "correct_answer": "Compare financial performance across periods and against peers to support investment and management decisions"
    },
    {
        "question": "The Net Profit Margin is calculated as:",
        "options": ["Gross Profit / Revenue x 100", "Net Profit After Tax / Revenue x 100", "Operating Profit / Total Assets x 100", "EBITDA / Total Equity x 100"],
        "correct_answer": "Net Profit After Tax / Revenue x 100"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "diploma.*financial.*accounting", "$options": "i"}})
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
        "title": "Diploma in Financial Accounting - Final Assessment",
        "description": "Test your knowledge of financial accounting principles, balance sheet components, financial statements and ratio analysis. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
