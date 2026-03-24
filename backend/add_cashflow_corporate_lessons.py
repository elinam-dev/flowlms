#!/usr/bin/env python3
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

LESSONS = [
    {"title": "Introduction to Cash Flow", "type": "embed", "content": "https://player.vimeo.com/video/908007535?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Types of Cash Flow", "type": "embed", "content": "https://player.vimeo.com/video/908007573?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Investing and Financial Activities", "type": "embed", "content": "https://player.vimeo.com/video/908007602?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Examples of Financing Activities and Cash Generation", "type": "embed", "content": "https://player.vimeo.com/video/908007641?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cash Flow From Investing Activities and Financing Activities", "type": "embed", "content": "https://player.vimeo.com/video/908007683?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Keshav Ltd Cash Flow Statement", "type": "embed", "content": "https://player.vimeo.com/video/908007729?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Consumption of Materials", "type": "embed", "content": "https://player.vimeo.com/video/908007761?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Profit and Loss Cash Flow Statement", "type": "embed", "content": "https://player.vimeo.com/video/908007794?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Net Cash Flow from Investing Activities", "type": "embed", "content": "https://player.vimeo.com/video/908007823?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Financial Accounting Diagram 8", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting8.jpeg"},
    {"title": "Financial Accounting Diagram 9", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting9.jpeg"},
    {"title": "Introduction to Corporate Governance", "type": "embed", "content": "https://player.vimeo.com/video/908007855?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Shareholders and Corporate Structure", "type": "embed", "content": "https://player.vimeo.com/video/908007890?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Anglo-US, Japanese-German, and Chinese Models", "type": "embed", "content": "https://player.vimeo.com/video/908007933?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Corporate Governance in India", "type": "embed", "content": "https://player.vimeo.com/video/908007965?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Enron Corporation", "type": "embed", "content": "https://player.vimeo.com/video/908008004?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Bankruptcy and Problems of Corporate Control", "type": "embed", "content": "https://player.vimeo.com/video/908008031?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Financial Accounting Diagram 10", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting10.jpeg"},
    {"title": "Financial Accounting Diagram 11", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting11.jpeg"},
    {"title": "Financial Accounting Diagram 12", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting12.jpeg"},
    {"title": "Financial Accounting Diagram 13", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting13.jpeg"},
    {"title": "Accounting Principles and Concepts", "type": "embed", "content": "https://player.vimeo.com/video/908008075?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Accounting Standards", "type": "embed", "content": "https://player.vimeo.com/video/908008110?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Evolution of Accounting", "type": "embed", "content": "https://player.vimeo.com/video/908008154?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Recording of Transactions", "type": "embed", "content": "https://player.vimeo.com/video/908008191?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Preparation and Summary of Financial Statement", "type": "embed", "content": "https://player.vimeo.com/video/908008222?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Financial Accounting Diagram 14", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting14.jpeg"},
    {"title": "Financial Accounting Diagram 15", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting15.jpeg"},
    {"title": "Financial Statement Analysis", "type": "embed", "content": "https://player.vimeo.com/video/908008249?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Financial Statement for Zee TV", "type": "embed", "content": "https://player.vimeo.com/video/908008275?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Balance Sheet for Zee TV", "type": "embed", "content": "https://player.vimeo.com/video/908008303?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Hindalco Industries Ltd", "type": "embed", "content": "https://player.vimeo.com/video/908008330?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Balance Sheet for Hindalco Industries Ltd", "type": "embed", "content": "https://player.vimeo.com/video/908008362?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Solution for Hindalco Industries Ltd Balance Sheet", "type": "embed", "content": "https://player.vimeo.com/video/908008396?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cash Flow Standalone Statement", "type": "embed", "content": "https://player.vimeo.com/video/908008431?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Financial Accounting Diagram 16", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting16.jpeg"},
    {"title": "Financial Accounting Diagram 17", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting17.jpeg"},
    {"title": "Horizontal, Vertical, and Ratio Analysis", "type": "embed", "content": "https://player.vimeo.com/video/908008463?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Classification of Ratios", "type": "embed", "content": "https://player.vimeo.com/video/908008496?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Calculation of Ratios I", "type": "embed", "content": "https://player.vimeo.com/video/908008526?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Calculation of Ratios II", "type": "embed", "content": "https://player.vimeo.com/video/908008569?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Review of Ratios and Profitability Ratios", "type": "embed", "content": "https://player.vimeo.com/video/908008605?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Return Ratios", "type": "embed", "content": "https://player.vimeo.com/video/908008640?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case Study: Financial Statement for Shipping Corp. of India", "type": "embed", "content": "https://player.vimeo.com/video/908008693?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Long Term Borrowing and Asset", "type": "embed", "content": "https://player.vimeo.com/video/908008734?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Common Size Statement and Comparative Balance Sheet", "type": "embed", "content": "https://player.vimeo.com/video/908008767?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cash Flow Statement", "type": "embed", "content": "https://player.vimeo.com/video/908008796?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Trend Analysis", "type": "embed", "content": "https://player.vimeo.com/video/908008827?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Leverage Ratios", "type": "embed", "content": "https://player.vimeo.com/video/908008858?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Calculating ROE, ROI, and Activity Ratios", "type": "embed", "content": "https://player.vimeo.com/video/908008896?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Financial Accounting Diagram 18", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting18.jpeg"},
    {"title": "Financial Accounting Diagram 19", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting19.jpeg"},
    {"title": "Financial Accounting Diagram 20", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting20.jpeg"}
]

async def add_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*financial.*accounting", "$options": "i"}
    })
    
    if not course:
        print("Course not found")
        return
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    if not module:
        print("Module not found")
        return
    
    existing_count = await db.lessons.count_documents({"module_id": module["id"]})
    
    for i, lesson_data in enumerate(LESSONS, start=existing_count):
        if lesson_data["type"] == "embed":
            content = f'<div style="text-align: center;"><iframe src="{lesson_data["content"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
        else:
            content = f'<div style="text-align: center; padding: 20px;"><img src="{lesson_data["content"]}" alt="{lesson_data["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson_data["title"],
            "content_type": "text" if lesson_data["type"] == "image" else "embed",
            "content": content,
            "duration_minutes": 10 if lesson_data["type"] == "embed" else 5,
            "order": i
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"Added: {lesson_data['title']}")
    
    print(f"\nAdded {len(LESSONS)} lessons")

if __name__ == "__main__":
    asyncio.run(add_lessons())
