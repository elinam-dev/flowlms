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
    {"title": "Financial Statements and Bank Transactions", "type": "embed", "content": vid("https://player.vimeo.com/video/453235623?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Current Liability", "type": "embed", "content": vid("https://player.vimeo.com/video/453235903?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Company Finances", "type": "embed", "content": vid("https://player.vimeo.com/video/453236098?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Purchases", "type": "embed", "content": vid("https://player.vimeo.com/video/453236386?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Overview of Discounts and Sales", "type": "embed", "content": vid("https://player.vimeo.com/video/453236651?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Analyzing a Sales Transaction", "type": "embed", "content": vid("https://player.vimeo.com/video/453236944?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Valuing Assets, Liabilities, and Expenditure", "type": "embed", "content": vid("https://player.vimeo.com/video/453237170?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Losses, Corporate Bonds and Interest", "type": "embed", "content": vid("https://player.vimeo.com/video/453237399?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Effects of Transactions on Bank Accounts and Carriage", "type": "embed", "content": vid("https://player.vimeo.com/video/455375338?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Dividend and Taxes Calculation", "type": "embed", "content": vid("https://player.vimeo.com/video/455379585?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "How Depreciation Comes in", "type": "embed", "content": vid("https://player.vimeo.com/video/455384272?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Assumptions in Financial Statements", "type": "embed", "content": vid("https://player.vimeo.com/video/455388220?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Yearly Closing Balance Sheets", "type": "embed", "content": vid("https://player.vimeo.com/video/461202172?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Yearly Closing Balance Sheets (Part 2)", "type": "embed", "content": vid("https://player.vimeo.com/video/461202172?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Yearly Closing Balance Sheets (Part 3)", "type": "embed", "content": vid("https://player.vimeo.com/video/461202534?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Authorized Capital", "type": "embed", "content": vid("https://player.vimeo.com/video/458120614?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Lone Pine Cafe Example", "type": "embed", "content": vid("https://player.vimeo.com/video/458124385?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Creating Real Life Scenarios", "type": "embed", "content": vid("https://player.vimeo.com/video/458131336?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Capital Gains and Liabilities", "type": "embed", "content": vid("https://player.vimeo.com/video/455498543?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Preparing the Balance Sheets", "type": "embed", "content": vid("https://player.vimeo.com/video/455511261?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Profit and Loss Calculations", "type": "embed", "content": vid("https://player.vimeo.com/video/455682753?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Amortization and Insurance", "type": "embed", "content": vid("https://player.vimeo.com/video/455685300?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Introduction to Journals or Ledgers", "type": "embed", "content": vid("https://player.vimeo.com/video/455685642?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Bank Accounts", "type": "embed", "content": vid("https://player.vimeo.com/video/455687851?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Diploma in Decision Making - Slide 4", "type": "text", "content": img(4)},
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
