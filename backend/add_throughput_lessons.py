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

lessons_data = [
    {"title": "Essentials of Throughput Accounting - Slide 1", "type": "text", "content": '<div style="text-align: center;"><img src="http://localhost:8000/uploads/images/Finance/essentials _of_throughput_accounting/essentials _of_throughput_accounting1.jpeg" alt="Slide 1" style="max-width: 100%; height: auto;" /></div>'},
    {"title": "Course Introduction", "type": "embed", "content": "https://player.vimeo.com/video/593773761?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Theory of Constraints", "type": "embed", "content": "https://player.vimeo.com/video/593777310?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Throughput Accounting", "type": "embed", "content": "https://player.vimeo.com/video/593783879?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Throughput Accounting Metrics", "type": "embed", "content": "https://player.vimeo.com/video/593786361?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Throughput Accounting Example", "type": "embed", "content": "https://player.vimeo.com/video/593788093?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction to Lean Accounting", "type": "embed", "content": "https://player.vimeo.com/video/593790886?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Lean Performance Measures", "type": "embed", "content": "https://player.vimeo.com/video/593842353?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Creating Lean Performance Measures", "type": "embed", "content": "https://player.vimeo.com/video/593844628?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Knowledge Test 1", "type": "embed", "content": "https://player.vimeo.com/video/593854089?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Manage by Value Stream", "type": "embed", "content": "https://player.vimeo.com/video/593865153?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Lean Accounting Tools", "type": "embed", "content": "https://player.vimeo.com/video/593865962?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Box Score Example", "type": "embed", "content": "https://player.vimeo.com/video/593870975?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Transaction Elimination", "type": "embed", "content": "https://player.vimeo.com/video/593876056?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Quantifying the Benefits of Lean Improvements", "type": "embed", "content": "https://player.vimeo.com/video/593880729?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "The Voice of the Customer", "type": "embed", "content": "https://player.vimeo.com/video/593883573?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Plan by Value Stream", "type": "embed", "content": "https://player.vimeo.com/video/593884681?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Knowledge Test 2", "type": "embed", "content": "https://player.vimeo.com/video/594039013?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Lean Accounting Assignment", "type": "embed", "content": "https://player.vimeo.com/video/594040428?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Lean Accounting Assignment Answer", "type": "embed", "content": "https://player.vimeo.com/video/594041725?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Lesson Summary", "type": "embed", "content": "https://player.vimeo.com/video/594036659?quality=720p&audiotrack=main&texttrack=en"},
]

async def add_lessons():
    course = await db.courses.find_one({"id": "5dcf3289-dd1f-44cc-98ea-aa1345c89dde"})
    print(f"Course: {course['title']}")

    module = await db.modules.find_one({"course_id": course['id']})

    # Delete existing lesson
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
