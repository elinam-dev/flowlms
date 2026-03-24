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

BASE = "http://localhost:8000/uploads/images/Finance/fundamentals_of_budgeting"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/fundamentals_of_budgeting{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = [
    {"title": "Fundamentals of Budgeting - Slide 1", "type": "text", "content": img(1)},
    {"title": "Budgeting and Budgetary Control", "type": "embed", "content": vid("https://player.vimeo.com/video/469593053?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Advantages of Budgetary Control System", "type": "embed", "content": vid("https://player.vimeo.com/video/469593427?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Illustration1 Material Purchase Budget", "type": "embed", "content": vid("https://player.vimeo.com/video/469593817?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Gauri Ltd Budget", "type": "embed", "content": vid("https://player.vimeo.com/video/469593965?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Vaibhav Ltd Cash Budget", "type": "embed", "content": vid("https://player.vimeo.com/video/469594096?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Cash Budget for the First Six Months", "type": "embed", "content": vid("https://player.vimeo.com/video/469594277?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Fundamentals of Budgeting - Slide 2", "type": "text", "content": img(2)},
    {"title": "Fundamentals of Budgeting - Slide 3", "type": "text", "content": img(3)},
    {"title": "Introduction to Standard Costing", "type": "embed", "content": vid("https://player.vimeo.com/video/469594516?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Variance", "type": "embed", "content": vid("https://player.vimeo.com/video/469594720?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Variance Analysis", "type": "embed", "content": vid("https://player.vimeo.com/video/469594926?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Material Variance", "type": "embed", "content": vid("https://player.vimeo.com/video/469595182?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Labour and Sales Variance", "type": "embed", "content": vid("https://player.vimeo.com/video/469595389?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Brahma Ltd Case", "type": "embed", "content": vid("https://player.vimeo.com/video/469595600?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Mahadev Ltd Case", "type": "embed", "content": vid("https://player.vimeo.com/video/469595792?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Fundamentals of Budgeting - Slide 4", "type": "text", "content": img(4)},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "6baf5c3e-6b9d-490b-a67e-ebf2a2533b73"})
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
