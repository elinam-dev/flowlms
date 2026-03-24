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

BASE = "http://localhost:8000/uploads/images/Finance/tax_accounting"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/tax_accounting{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = [
    {"title": "Tax Accounting - Slide 1", "type": "text", "content": img(1)},
    {"title": "Tax System and Administration in the UK", "type": "embed", "content": vid("https://player.vimeo.com/video/700035825?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Tax on Individuals", "type": "embed", "content": vid("https://player.vimeo.com/video/700036259?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "National Insurance", "type": "embed", "content": vid("https://player.vimeo.com/video/700037176?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "How to Submit a Self-Assessment Tax Return", "type": "embed", "content": vid("https://player.vimeo.com/video/700037503?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Fundamentals of Income Tax", "type": "embed", "content": vid("https://player.vimeo.com/video/700037997?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Advanced Income Tax", "type": "embed", "content": vid("https://player.vimeo.com/video/700038674?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Advanced Income Tax: Trading Income Tax", "type": "embed", "content": vid("https://player.vimeo.com/video/701037053?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Payee, Payroll and Wages", "type": "embed", "content": vid("https://player.vimeo.com/video/700039708?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Capital Gain Tax", "type": "embed", "content": vid("https://player.vimeo.com/video/700040261?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Value Added Tax", "type": "embed", "content": vid("https://player.vimeo.com/video/700040797?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Import and Export", "type": "embed", "content": vid("https://player.vimeo.com/video/700042606?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Corporation Tax", "type": "embed", "content": vid("https://player.vimeo.com/video/700043237?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Inheritance Tax", "type": "embed", "content": vid("https://player.vimeo.com/video/700043819?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Double Entry Accounting", "type": "embed", "content": vid("https://player.vimeo.com/video/700044241?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Management Accounting and Financial Analysis", "type": "embed", "content": vid("https://player.vimeo.com/video/700045597?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Career as a Tax Accountant in the UK", "type": "embed", "content": vid("https://player.vimeo.com/video/700045988?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Lesson Summary - Slide 2", "type": "text", "content": img(2)},
    {"title": "Lesson Summary - Slide 3", "type": "text", "content": img(3)},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "3cf997a2-b127-4db7-a442-0febc3f2d51e"})
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
