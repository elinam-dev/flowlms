import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "The Current Ratio is calculated as:",
        "options": ["Total Assets / Total Liabilities", "Current Assets / Current Liabilities", "Net Profit / Total Assets", "Current Liabilities / Current Assets"],
        "correct_answer": "Current Assets / Current Liabilities"
    },
    {
        "question": "A Current Ratio of less than 1 indicates:",
        "options": ["The company is highly profitable", "The company may struggle to meet its short-term obligations", "The company has no long-term debt", "The company is over-capitalised"],
        "correct_answer": "The company may struggle to meet its short-term obligations"
    },
    {
        "question": "The Quick Ratio (Acid Test) excludes which asset from its calculation?",
        "options": ["Cash and cash equivalents", "Trade receivables", "Inventory", "Short-term investments"],
        "correct_answer": "Inventory"
    },
    {
        "question": "Return on Equity (ROE) measures:",
        "options": ["How efficiently a company uses its total assets to generate profit", "The profit generated for every unit of shareholders' equity", "The ratio of debt to equity in the capital structure", "The gross profit as a percentage of revenue"],
        "correct_answer": "The profit generated for every unit of shareholders' equity"
    },
    {
        "question": "The Gross Profit Margin is calculated as:",
        "options": ["Net Profit / Revenue x 100", "(Revenue - Cost of Goods Sold) / Revenue x 100", "Operating Profit / Total Assets x 100", "EBIT / Revenue x 100"],
        "correct_answer": "(Revenue - Cost of Goods Sold) / Revenue x 100"
    },
    {
        "question": "The Debt-to-Equity Ratio is used to assess:",
        "options": ["A company's short-term liquidity", "The proportion of financing from debt versus equity", "How quickly inventory is sold", "The efficiency of asset utilisation"],
        "correct_answer": "The proportion of financing from debt versus equity"
    },
    {
        "question": "A high Inventory Turnover Ratio generally indicates:",
        "options": ["Slow-moving stock and potential obsolescence", "Efficient inventory management and strong sales", "Excessive investment in fixed assets", "Poor credit control"],
        "correct_answer": "Efficient inventory management and strong sales"
    },
    {
        "question": "The Price-to-Earnings (P/E) Ratio is primarily used by:",
        "options": ["Creditors to assess debt repayment ability", "Investors to evaluate whether a share is over or undervalued", "Management to control operating costs", "Auditors to verify financial statements"],
        "correct_answer": "Investors to evaluate whether a share is over or undervalued"
    },
    {
        "question": "Earnings Per Share (EPS) is calculated as:",
        "options": ["Total Revenue / Number of Shares", "Net Profit After Tax / Number of Ordinary Shares in Issue", "Operating Profit / Total Equity", "Dividends Paid / Number of Shares"],
        "correct_answer": "Net Profit After Tax / Number of Ordinary Shares in Issue"
    },
    {
        "question": "The Debtor Days ratio measures:",
        "options": ["How many days on average it takes to sell inventory", "How many days on average it takes to collect payment from customers", "The number of days to pay suppliers", "The average length of the operating cycle"],
        "correct_answer": "How many days on average it takes to collect payment from customers"
    },
    {
        "question": "Return on Assets (ROA) indicates:",
        "options": ["How much profit is generated per unit of equity", "How efficiently a company uses its assets to generate profit", "The market value of the company's assets", "The ratio of current assets to total assets"],
        "correct_answer": "How efficiently a company uses its assets to generate profit"
    },
    {
        "question": "Horizontal analysis of financial statements involves:",
        "options": ["Comparing each line item as a percentage of a base figure within the same year", "Comparing financial data across multiple periods to identify trends", "Benchmarking against industry competitors", "Calculating financial ratios for a single period"],
        "correct_answer": "Comparing financial data across multiple periods to identify trends"
    },
    {
        "question": "Vertical analysis expresses each item in a financial statement as:",
        "options": ["A ratio compared to the prior year", "A percentage of a base figure such as total revenue or total assets", "An absolute monetary value", "A comparison against industry averages"],
        "correct_answer": "A percentage of a base figure such as total revenue or total assets"
    },
    {
        "question": "The Interest Coverage Ratio is calculated as:",
        "options": ["Net Profit / Interest Expense", "EBIT / Interest Expense", "Total Debt / Annual Interest", "Operating Cash Flow / Total Liabilities"],
        "correct_answer": "EBIT / Interest Expense"
    },
    {
        "question": "Which of the following is a limitation of ratio analysis?",
        "options": ["It provides too much detail about cash flows", "Ratios are based on historical data and may not reflect current conditions", "It cannot be used to compare companies in the same industry", "It always gives a complete picture of financial health"],
        "correct_answer": "Ratios are based on historical data and may not reflect current conditions"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "financial statement analysis", "$options": "i"}})
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
        "title": "Financial Statement Analysis - Final Assessment",
        "description": "Test your knowledge of accounting ratios, liquidity, profitability and analytical strategy. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
