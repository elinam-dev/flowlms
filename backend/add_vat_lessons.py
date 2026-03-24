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

BASE = "http://localhost:8000/uploads/images/Finance/basics_of_value-added_tax"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/basics_of_value-added_tax{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = [
    {"title": "Basics of Value-Added Tax - Slide 1", "type": "text", "content": img(1)},
    {"title": "Introducing VAT Concepts", "type": "embed", "content": vid("https://player.vimeo.com/video/753116306?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "VAT Mechanisms and Core Features", "type": "embed", "content": vid("https://player.vimeo.com/video/753117513?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "VAT System in the UK", "type": "embed", "content": vid("https://player.vimeo.com/video/753119064?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "VAT Impact of Finance Act 2021", "type": "embed", "content": vid("https://player.vimeo.com/video/753119567?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Learning Value-Added Tax Terminology", "type": "embed", "content": vid("https://player.vimeo.com/video/753120258?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Explaining Primary VAT Terms", "type": "embed", "content": vid("https://player.vimeo.com/video/753121010?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Methods of Calculating VAT Liability", "type": "embed", "content": vid("https://player.vimeo.com/video/753121799?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Describing Tax Responsibilities", "type": "embed", "content": vid("https://player.vimeo.com/video/753122945?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Defining Taxable Persons and Sellers", "type": "embed", "content": vid("https://player.vimeo.com/video/753124356?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Tax Collectible from Third Persons", "type": "embed", "content": vid("https://player.vimeo.com/video/753125155?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Understanding the VAT Registration", "type": "embed", "content": vid("https://player.vimeo.com/video/753126557?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "UK Value-Added Tax Registration Process", "type": "embed", "content": vid("https://player.vimeo.com/video/753128786?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Procedure for Cancelling the Registration", "type": "embed", "content": vid("https://player.vimeo.com/video/753130272?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Describing the VAT Rates in Different Countries", "type": "embed", "content": vid("https://player.vimeo.com/video/753131252?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Differentiating Standard and Reduced VAT Rates", "type": "embed", "content": vid("https://player.vimeo.com/video/753131803?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Explaining VAT Rates and Excise Duties", "type": "embed", "content": vid("https://player.vimeo.com/video/753132557?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Showing the Current VAT Rates in the UK", "type": "embed", "content": vid("https://player.vimeo.com/video/753133050?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Understanding a VAT Invoice", "type": "embed", "content": vid("https://player.vimeo.com/video/753133986?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Content Requirements in VAT Invoices", "type": "embed", "content": vid("https://player.vimeo.com/video/753135096?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Explaining VAT Sales Receipt and Record-Keeping", "type": "embed", "content": vid("https://player.vimeo.com/video/753135827?quality=720p&audiotrack=main&texttrack=en")},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "7cc7787d-8050-4432-a5ae-6fc22664fe18"})
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
