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

BASE = "http://localhost:8000/uploads/images/Finance/sage_one"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/sage_one{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

lessons_data = [
    {"title": "Sage One - Slide 1", "type": "text", "content": img(1)},
    {"title": "Downloading Sage & Signing Up", "type": "embed", "content": "https://player.vimeo.com/video/564469500?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Adding Customers & Suppliers", "type": "embed", "content": "https://player.vimeo.com/video/564475714?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Reviewing Charts of Accounts", "type": "embed", "content": "https://player.vimeo.com/video/564480022?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Entering Invoices", "type": "embed", "content": "https://player.vimeo.com/video/564614296?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Entering Credit Notes", "type": "embed", "content": "https://player.vimeo.com/video/564616511?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Correcting Invoice Entries & Wiping Data", "type": "embed", "content": "https://player.vimeo.com/video/564622888?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Printing & Mailing Invoices", "type": "embed", "content": "https://player.vimeo.com/video/564633574?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Printing & Mailing Credit Notes", "type": "embed", "content": "https://player.vimeo.com/video/561191388?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Sage One - Slide 2", "type": "text", "content": img(2)},
    {"title": "Sage One - Slide 3", "type": "text", "content": img(3)},
    {"title": "Entering Sales/Customer Receipts", "type": "embed", "content": "https://player.vimeo.com/video/564643135?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Paying Suppliers", "type": "embed", "content": "https://player.vimeo.com/video/564648840?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Reporting Money Received", "type": "embed", "content": "https://player.vimeo.com/video/564681557?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Non-Invoiced Payments & Cash Transactions", "type": "embed", "content": "https://player.vimeo.com/video/564691439?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Bank Reconciliation", "type": "embed", "content": "https://player.vimeo.com/video/564698751?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Generating Reports", "type": "embed", "content": "https://player.vimeo.com/video/564703380?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Sage One - Slide 4", "type": "text", "content": img(4)},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "c73a35db-27c1-47f0-871e-7993855f24d1"})
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
