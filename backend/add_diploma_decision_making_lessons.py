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

lessons_data = [
    {"title": "Diploma in Decision Making - Slide 1", "type": "text", "content": img(1)},
    {"title": "Introduction to Basic Accounting Concepts", "type": "embed", "content": vid("https://player.vimeo.com/video/453230337?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Working Examples", "type": "embed", "content": vid("https://player.vimeo.com/video/453230798?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Introduction to Balance Sheets", "type": "embed", "content": vid("https://player.vimeo.com/video/453230975?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Conservatism and Depreciation", "type": "embed", "content": vid("https://player.vimeo.com/video/453231398?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Concept of Value", "type": "embed", "content": vid("https://player.vimeo.com/video/453231969?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Expenditure and Liabilities", "type": "embed", "content": vid("https://player.vimeo.com/video/453232613?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "A Look at Balance Sheets", "type": "embed", "content": vid("https://player.vimeo.com/video/453233039?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Preference Shares and Investment Concepts", "type": "embed", "content": vid("https://player.vimeo.com/video/453233645?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Effects of Different Scenarios in Companies", "type": "embed", "content": vid("https://player.vimeo.com/video/453234042?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Market Related Concepts", "type": "embed", "content": vid("https://player.vimeo.com/video/453234635?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Inner Workings of Companies and Shareholders", "type": "embed", "content": vid("https://player.vimeo.com/video/453234829?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Investor's Formula", "type": "embed", "content": vid("https://player.vimeo.com/video/453235046?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Parts of a Transaction", "type": "embed", "content": vid("https://player.vimeo.com/video/453235374?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Diploma in Decision Making - Slide 2", "type": "text", "content": img(2)},
    {"title": "Diploma in Decision Making - Slide 3", "type": "text", "content": img(3)},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "c1fae7e5-41fe-4ab5-b6a2-61d759ecfa43"})
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
