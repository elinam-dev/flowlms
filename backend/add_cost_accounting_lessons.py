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

BASE = "http://localhost:8000/uploads/images/Finance/diploma_in_cost_accounting"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/diploma_in_cost_accounting{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

lessons_data = [
    {"title": "Diploma in Cost Accounting - Slide 1", "type": "text", "content": img(1)},
    {"title": "What is Cost Accounting?", "type": "embed", "content": "https://player.vimeo.com/video/471420963?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cost and Management Accounting", "type": "embed", "content": "https://player.vimeo.com/video/471420658?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cost Classification", "type": "embed", "content": "https://player.vimeo.com/video/471421528?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cost Classification (contd)", "type": "embed", "content": "https://player.vimeo.com/video/471421163?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cost Volume Profit (CVP)", "type": "embed", "content": "https://player.vimeo.com/video/471421721?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cost Volume Profit Analysis", "type": "embed", "content": "https://player.vimeo.com/video/471422410?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cost Graphs and CVP", "type": "embed", "content": "https://player.vimeo.com/video/471423288?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Breakeven Point (BEP)", "type": "embed", "content": "https://player.vimeo.com/video/471423135?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "PV Ratio", "type": "embed", "content": "https://player.vimeo.com/video/471424087?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Marginal/Variable Costing", "type": "embed", "content": "https://player.vimeo.com/video/471423872?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Diploma in Cost Accounting - Slide 2", "type": "text", "content": img(2)},
    {"title": "Diploma in Cost Accounting - Slide 3", "type": "text", "content": img(3)},
    {"title": "CVP BEP Case Solutions", "type": "embed", "content": "https://player.vimeo.com/video/471424441?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "CVP BEP Case Solutions (contd)", "type": "embed", "content": "https://player.vimeo.com/video/471424343?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Sensitivity Analysis", "type": "embed", "content": "https://player.vimeo.com/video/471689750?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case of Ayur Pharma", "type": "embed", "content": "https://player.vimeo.com/video/471424911?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case of Ayur Pharma (contd)", "type": "embed", "content": "https://player.vimeo.com/video/471424668?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case of Profit Planning", "type": "embed", "content": "https://player.vimeo.com/video/471425369?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Case of Profit Planning (contd)", "type": "embed", "content": "https://player.vimeo.com/video/471425081?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Relevant vs Sunk Cost", "type": "embed", "content": "https://player.vimeo.com/video/471425768?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Other Scenarios in Decision Making", "type": "embed", "content": "https://player.vimeo.com/video/471425581?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Diploma in Cost Accounting - Slide 4", "type": "text", "content": img(4)},
    {"title": "Diploma in Cost Accounting - Slide 5", "type": "text", "content": img(5)},
    {"title": "Rhishi Prashala Case", "type": "embed", "content": "https://player.vimeo.com/video/469590749?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Calculating BEP and PV Ratio", "type": "embed", "content": "https://player.vimeo.com/video/469590900?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Profit and Loss Account of JSW ISPAT Steel", "type": "embed", "content": "https://player.vimeo.com/video/469591113?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Profit and Loss Account Decision Making", "type": "embed", "content": "https://player.vimeo.com/video/469591372?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Divya Aushadi Ltd", "type": "embed", "content": "https://player.vimeo.com/video/469591557?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Income Statement and Tax", "type": "embed", "content": "https://player.vimeo.com/video/469592053?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Shree Cements", "type": "embed", "content": "https://player.vimeo.com/video/469592484?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Normal and Concessional Selling Price", "type": "embed", "content": "https://player.vimeo.com/video/469592748?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Diploma in Cost Accounting - Slide 6", "type": "text", "content": img(6)},
    {"title": "Diploma in Cost Accounting - Slide 7", "type": "text", "content": img(7)},
    {"title": "Introduction to Budgeting", "type": "embed", "content": "https://player.vimeo.com/video/469593053?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Advantages of Budgetary Control System", "type": "embed", "content": "https://player.vimeo.com/video/469593427?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Illustration1 Material Purchase Budget", "type": "embed", "content": "https://player.vimeo.com/video/469593817?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Gauri Ltd Budget", "type": "embed", "content": "https://player.vimeo.com/video/469593965?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Vaibhav Ltd Cash Budget", "type": "embed", "content": "https://player.vimeo.com/video/469594096?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Cash Budget for the First Six Months", "type": "embed", "content": "https://player.vimeo.com/video/469594277?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction to Standard Costing", "type": "embed", "content": "https://player.vimeo.com/video/469594516?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Variance", "type": "embed", "content": "https://player.vimeo.com/video/469594720?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Variance Analysis", "type": "embed", "content": "https://player.vimeo.com/video/469594926?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Material Variance", "type": "embed", "content": "https://player.vimeo.com/video/469595182?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Labour and Sales Variance", "type": "embed", "content": "https://player.vimeo.com/video/469595389?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Brahma Ltd Case", "type": "embed", "content": "https://player.vimeo.com/video/469595600?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Mahadev Ltd Case", "type": "embed", "content": "https://player.vimeo.com/video/469595792?quality=720p&audiotrack=main&texttrack=en"},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "3e5143d8-e3ff-489a-a728-81d059b85787"})
    print(f"Course: {course['title']}")

    module = await db.modules.find_one({"course_id": course['id']})

    # Delete existing lessons
    await db.lessons.delete_many({"module_id": module['id']})

    for i, lesson in enumerate(lessons_data):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module['id'],
            "title": lesson['title'],
            "content_type": lesson['type'],
            "content": lesson['content'],
            "duration_minutes": 10,
            "order": i
        })

    print(f"Added {len(lessons_data)} lessons")

if __name__ == "__main__":
    asyncio.run(add_lessons())
