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
    {"title": "Introduction to Accounting", "type": "embed", "content": "https://player.vimeo.com/video/908006302?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Streams of Accounting", "type": "embed", "content": "https://player.vimeo.com/video/908006330?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Financial Statement of an Organization", "type": "embed", "content": "https://player.vimeo.com/video/908006376?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction to Basic Business Models", "type": "embed", "content": "https://player.vimeo.com/video/908006422?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Balance Sheet", "type": "embed", "content": "https://player.vimeo.com/video/908006445?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "The Items in a Balance Sheet", "type": "embed", "content": "https://player.vimeo.com/video/908006468?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Short Balance Sheet", "type": "embed", "content": "https://player.vimeo.com/video/908006503?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Detailed Balance Sheet", "type": "embed", "content": "https://player.vimeo.com/video/908006532?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Non-Current and Current Liabilities", "type": "embed", "content": "https://player.vimeo.com/video/908006578?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Review of Liabilities in Balance Sheet", "type": "embed", "content": "https://player.vimeo.com/video/908006605?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Assets in Balance Sheet", "type": "embed", "content": "https://player.vimeo.com/video/908006635?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Types of Assets", "type": "embed", "content": "https://player.vimeo.com/video/908006684?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Problem 1", "type": "embed", "content": "https://player.vimeo.com/video/908006705?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Problem 2", "type": "embed", "content": "https://player.vimeo.com/video/908006732?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Problem 3", "type": "embed", "content": "https://player.vimeo.com/video/908006760?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Review of Assets in Balance Sheet", "type": "embed", "content": "https://player.vimeo.com/video/908006795?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Fixed Assets", "type": "embed", "content": "https://player.vimeo.com/video/908006820?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Liabilities and Types of Liabilities", "type": "embed", "content": "https://player.vimeo.com/video/908006856?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Provision", "type": "embed", "content": "https://player.vimeo.com/video/908006899?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Contingent Liability and Owners Funds", "type": "embed", "content": "https://player.vimeo.com/video/908006916?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Balance Sheet Equation", "type": "embed", "content": "https://player.vimeo.com/video/908006952?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Financial Accounting Diagram 1", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting2.jpeg"},
    {"title": "Financial Accounting Diagram 2", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting3.jpeg"},
    {"title": "Financial Accounting Diagram 3", "type": "image", "content": "/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting4.jpeg"},
    {"title": "Elements of Profit and Loss Account", "type": "embed", "content": "https://player.vimeo.com/video/908006977?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Company Act Formats (Heading I - IV)", "type": "embed", "content": "https://player.vimeo.com/video/908006998?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Company Act Formats (Heading V - XV)", "type": "embed", "content": "https://player.vimeo.com/video/908007041?quality=720p&audiotrack=main&texttrack=en"}
]

async def add_diploma_accounting_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*financial.*accounting", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    # Update first lesson
    lesson1 = await db.lessons.find_one({
        "module_id": module["id"],
        "title": "Introduction"
    })
    
    if lesson1:
        content = '<div style="text-align: center; padding: 20px;"><img src="/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting1.jpeg" alt="Introduction" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        await db.lessons.update_one(
            {"id": lesson1["id"]},
            {"$set": {"content": content, "content_type": "text"}}
        )
        print(f"Updated: Introduction")
    
    # Add remaining lessons
    for i, lesson_data in enumerate(LESSONS, start=1):
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
    asyncio.run(add_diploma_accounting_lessons())
