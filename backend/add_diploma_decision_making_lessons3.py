import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

BASE = "http://localhost:8000/uploads/images/Finance/diploma_in_decision_making"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/diploma_in_decision_making{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

new_lessons = [
    {"title": "Diploma in Decision Making - Slide 5", "type": "text", "content": img(5)},
    {"title": "The Nardkani Ledger Example", "type": "embed", "content": vid("https://player.vimeo.com/video/455689614?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Conclusions From Nardkani Ledger", "type": "embed", "content": vid("https://player.vimeo.com/video/455690783?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Vijay Merchants Example Transaction", "type": "embed", "content": vid("https://player.vimeo.com/video/455693458?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Recording Sample Sales and Payments", "type": "embed", "content": vid("https://player.vimeo.com/video/455694106?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "How Transactions Affect Books and Goods", "type": "embed", "content": vid("https://player.vimeo.com/video/455696076?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Additional Vijay Merchants Sample Sales", "type": "embed", "content": vid("https://player.vimeo.com/video/455699028?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "How Journals are Balanced After Expenditure", "type": "embed", "content": vid("https://player.vimeo.com/video/455700493?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Introduction to Ledger Posting", "type": "embed", "content": vid("https://player.vimeo.com/video/455701661?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Balancing Different Accounts", "type": "embed", "content": vid("https://player.vimeo.com/video/455703007?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Sales Account Transactions", "type": "embed", "content": vid("https://player.vimeo.com/video/455705169?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Getting Your Cash Net Balance", "type": "embed", "content": vid("https://player.vimeo.com/video/455706430?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Setting up the Final Ledger", "type": "embed", "content": vid("https://player.vimeo.com/video/455707785?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Recording Sales and Purchases in our Profit and Loss Sheet", "type": "embed", "content": vid("https://player.vimeo.com/video/455708771?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Representing Assets and Liabilities", "type": "embed", "content": vid("https://player.vimeo.com/video/455711013?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Diploma in Decision Making - Slide 6", "type": "text", "content": img(6)},
    {"title": "Diploma in Decision Making - Slide 7", "type": "text", "content": img(7)},
    {"title": "Introduction to Cash Flow Statement", "type": "embed", "content": vid("https://player.vimeo.com/video/455714282?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Cost of Goods Sold and Inventories", "type": "embed", "content": vid("https://player.vimeo.com/video/455716833?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Opening and Closing Inventories - Examples", "type": "embed", "content": vid("https://player.vimeo.com/video/455718254?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Insurance and Taxes", "type": "embed", "content": vid("https://player.vimeo.com/video/455719818?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Introduction to Cashflow", "type": "embed", "content": vid("https://player.vimeo.com/video/455721036?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Getting Cashflow from Company Operations", "type": "embed", "content": vid("https://player.vimeo.com/video/455722916?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Direct and Indirect Methods of Preparing Cash Flow Statements", "type": "embed", "content": vid("https://player.vimeo.com/video/458133690?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Creditor Calculations", "type": "embed", "content": vid("https://player.vimeo.com/video/458138869?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Cashflow in Relation to Taxes", "type": "embed", "content": vid("https://player.vimeo.com/video/455734050?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Closing Balances and Conclusions", "type": "embed", "content": vid("https://player.vimeo.com/video/455735618?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Issue of Share Capital", "type": "embed", "content": vid("https://player.vimeo.com/video/457634868?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Cash Inflow and Outflow", "type": "embed", "content": vid("https://player.vimeo.com/video/457633520?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Diploma in Decision Making - Slide 8", "type": "text", "content": img(8)},
    {"title": "Diploma in Decision Making - Slide 9", "type": "text", "content": img(9)},
    {"title": "Consolidated Balance Sheet", "type": "embed", "content": vid("https://player.vimeo.com/video/457633958?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Authorized Capital", "type": "embed", "content": vid("https://player.vimeo.com/video/457629581?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Non-Current Liabilities", "type": "embed", "content": vid("https://player.vimeo.com/video/457635409?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Financial Liabilities Payable", "type": "embed", "content": vid("https://player.vimeo.com/video/457634640?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Value of Machinery", "type": "embed", "content": vid("https://player.vimeo.com/video/457635930?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Current Assets", "type": "embed", "content": vid("https://player.vimeo.com/video/457636362?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Loan Provider and Performance Ratios", "type": "embed", "content": vid("https://player.vimeo.com/video/457708971?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Liquidity and Current Ratio", "type": "embed", "content": vid("https://player.vimeo.com/video/457704510?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Debt by Equity Ratio", "type": "embed", "content": vid("https://player.vimeo.com/video/458905319?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Recession in the Economy", "type": "embed", "content": vid("https://player.vimeo.com/video/458905930?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Diploma in Decision Making - Slide 10", "type": "text", "content": img(10)},
    {"title": "Diploma in Decision Making - Slide 11", "type": "text", "content": img(11)},
    {"title": "Return on Equity", "type": "embed", "content": vid("https://player.vimeo.com/video/457636749?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Liquidity Ratios", "type": "embed", "content": vid("https://player.vimeo.com/video/457637994?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Profitability Ratio", "type": "embed", "content": vid("https://player.vimeo.com/video/457684674?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Ratio Analysis (Debt/Equity)", "type": "embed", "content": vid("https://player.vimeo.com/video/457686147?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Ratio Analysis (Working Capital)", "type": "embed", "content": vid("https://player.vimeo.com/video/457698216?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Ratio Analysis (Vendor)", "type": "embed", "content": vid("https://player.vimeo.com/video/457693579?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Measuring Profitability", "type": "embed", "content": vid("https://player.vimeo.com/video/457700570?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Return on Investment (ROI)", "type": "embed", "content": vid("https://player.vimeo.com/video/457700959?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Balance Sheet (Assets and Liabilities)", "type": "embed", "content": vid("https://player.vimeo.com/video/457680033?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Equity Capital (Reserves and Surplus)", "type": "embed", "content": vid("https://player.vimeo.com/video/457681944?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Capital Structure (Equity and Debt)", "type": "embed", "content": vid("https://player.vimeo.com/video/457680991?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Operating (Cash Inflow/Outflow)", "type": "embed", "content": vid("https://player.vimeo.com/video/457682728?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Diploma in Decision Making - Slide 11", "type": "text", "content": img(11)},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "c1fae7e5-41fe-4ab5-b6a2-61d759ecfa43"})
    print(f"Course: {course['title']}")

    module = await db.modules.find_one({"course_id": course['id']})
    current_count = await db.lessons.count_documents({"module_id": module['id']})
    print(f"Existing lessons: {current_count}")

    for i, lesson in enumerate(new_lessons):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module['id'],
            "title": lesson['title'],
            "content_type": lesson['type'],
            "content": lesson['content'],
            "duration_minutes": 10,
            "order": current_count + i
        })

    print(f"Added {len(new_lessons)} lessons. Total: {current_count + len(new_lessons)}")

if __name__ == "__main__":
    asyncio.run(add_lessons())
