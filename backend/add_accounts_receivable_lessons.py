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

BASE = "http://localhost:8000/uploads/images/Finance/accounts_receive_able_management"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/accounts_receive_able_management{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = [
    {"title": "Accounts Receivable Management - Slide 1", "type": "text", "content": img(1)},
    {"title": "What Are Accounts Receivable", "type": "embed", "content": vid("https://player.vimeo.com/video/870791555?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Accounts Receivable Terminology", "type": "embed", "content": vid("https://player.vimeo.com/video/870792138?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Accounts Receivable Process Flow", "type": "embed", "content": vid("https://player.vimeo.com/video/870792637?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Credit Policies and Procedures", "type": "embed", "content": vid("https://player.vimeo.com/video/870795776?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Credit Assessment and Risk Analysis", "type": "embed", "content": vid("https://player.vimeo.com/video/870797804?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Billing and Invoicing", "type": "embed", "content": vid("https://player.vimeo.com/video/870799232?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Receivables Collection Strategies", "type": "embed", "content": vid("https://player.vimeo.com/video/870805870?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Cash Application and Reconciliation", "type": "embed", "content": vid("https://player.vimeo.com/video/870806372?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Accounts Receivable Technologies and Trends", "type": "embed", "content": vid("https://player.vimeo.com/video/870808864?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Accounts Receivable Management - Slide 2", "type": "text", "content": img(2)},
    {"title": "Accounts Receivable Management - Slide 3", "type": "text", "content": img(3)},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "173a7bfb-e8c3-47e4-bdb5-91a3e1dc3c47"})
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
