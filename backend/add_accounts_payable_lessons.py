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

BASE = "http://localhost:8000/uploads/images/Finance/accounts_payable_management"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/accounts_payable_management{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = [
    {"title": "Accounts Payable Management - Slide 1", "type": "text", "content": img(1)},
    {"title": "Introduction to Accounts Payable Management", "type": "embed", "content": vid("https://player.vimeo.com/video/1010849933?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Importance of Efficient Account Payable Processes", "type": "embed", "content": vid("https://player.vimeo.com/video/1010850369?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Overview of Accounts Payable Systems and Software", "type": "embed", "content": vid("https://player.vimeo.com/video/1010850802?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Best Practices in Accounts Payable Management", "type": "embed", "content": vid("https://player.vimeo.com/video/1010851722?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Invoice Processing", "type": "embed", "content": vid("https://player.vimeo.com/video/1010855120?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Invoice Verification and Matching", "type": "embed", "content": vid("https://player.vimeo.com/video/1010856199?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Handling Discrepancies", "type": "embed", "content": vid("https://player.vimeo.com/video/1010857062?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Payment Processing", "type": "embed", "content": vid("https://player.vimeo.com/video/1010859551?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Payment Authorisation", "type": "embed", "content": vid("https://player.vimeo.com/video/1010869452?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Fraud Prevention in Payments", "type": "embed", "content": vid("https://player.vimeo.com/video/1010871135?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Vendor Management", "type": "embed", "content": vid("https://player.vimeo.com/video/1011624356?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Vendor Performance Evaluation", "type": "embed", "content": vid("https://player.vimeo.com/video/1010874464?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Expense Management", "type": "embed", "content": vid("https://player.vimeo.com/video/1010875451?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Expense Auditing", "type": "embed", "content": vid("https://player.vimeo.com/video/1010878005?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Tracking and Reporting Expenses", "type": "embed", "content": vid("https://player.vimeo.com/video/1010879528?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Financial Controls and Audits", "type": "embed", "content": vid("https://player.vimeo.com/video/1010883423?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Audit Preparation and Procedures", "type": "embed", "content": vid("https://player.vimeo.com/video/1010885673?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Identifying and Mitigating Risks", "type": "embed", "content": vid("https://player.vimeo.com/video/1010886468?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Reporting and Analysis", "type": "embed", "content": vid("https://player.vimeo.com/video/1011029381?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Month-End Closing Processes", "type": "embed", "content": vid("https://player.vimeo.com/video/1011030751?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Using Reports for Decision Making", "type": "embed", "content": vid("https://player.vimeo.com/video/1011031308?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Accounts Payable Management - Slide 2", "type": "text", "content": img(2)},
    {"title": "Accounts Payable Management - Slide 3", "type": "text", "content": img(3)},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "b1a49e34-d936-411e-a7f4-7fafde72a56c"})
    print(f"Course: {course['title']}")

    module = await db.modules.find_one({"course_id": course['id']})

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
