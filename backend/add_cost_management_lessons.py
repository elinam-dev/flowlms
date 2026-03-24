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

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = [
    {"title": "Learning Outcomes", "type": "embed", "content": vid("https://player.vimeo.com/video/856148811?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "The Purpose of Management Accounting", "type": "embed", "content": vid("https://player.vimeo.com/video/847168235?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Classification of Costs", "type": "embed", "content": vid("https://player.vimeo.com/video/847276413?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Foodly Inc.", "type": "embed", "content": vid("https://player.vimeo.com/video/847280686?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Decision-Making", "type": "embed", "content": vid("https://player.vimeo.com/video/847284000?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Marginal Costing", "type": "embed", "content": vid("https://player.vimeo.com/video/847299217?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Concept Review", "type": "embed", "content": vid("https://player.vimeo.com/video/852050664?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Foodly Inc. Example", "type": "embed", "content": vid("https://player.vimeo.com/video/853651066?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Cost-Volume-Profit Analysis Introduction", "type": "embed", "content": vid("https://player.vimeo.com/video/853656437?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Cost-Volume-Profit Analysis", "type": "embed", "content": vid("https://player.vimeo.com/video/853661438?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Foodly Inc. Contribution", "type": "embed", "content": vid("https://player.vimeo.com/video/851362196?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Cost Accounting", "type": "embed", "content": vid("https://player.vimeo.com/video/853625446?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Costing Systems", "type": "embed", "content": vid("https://player.vimeo.com/video/851376503?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Concept Review", "type": "embed", "content": vid("https://player.vimeo.com/video/853628443?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Lesson Summary", "type": "embed", "content": vid("https://player.vimeo.com/video/852065813?quality=720p&audiotrack=main&texttrack=en")},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "1a8b9fb1-d47b-47cd-9569-ce1ce1d313d7"})
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
