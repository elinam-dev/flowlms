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

BASE = "http://localhost:8000/uploads/images/Finance/the_accounting_cycle"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/the_accounting_cycle{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = (
    [{"title": f"The Accounting Cycle - Slide {i}", "type": "text", "content": img(i)} for i in range(1, 132)] +
    [
        {"title": "Analyze Transactions", "type": "embed", "content": vid("https://player.vimeo.com/video/552820438")},
        {"title": "Journalize Transactions", "type": "embed", "content": vid("https://player.vimeo.com/video/552820550")},
        {"title": "Post Transactions", "type": "embed", "content": vid("https://player.vimeo.com/video/552820675")},
        {"title": "Unadjusted Trial Balance (Corporations)", "type": "embed", "content": vid("https://player.vimeo.com/video/552820794")},
        {"title": "Adjusting Entries Basics", "type": "embed", "content": vid("https://player.vimeo.com/video/552820955")},
        {"title": "Adjusted Trial Balance for Corporations", "type": "embed", "content": vid("https://player.vimeo.com/video/552821148")},
        {"title": "Single-Step Income Statement", "type": "embed", "content": vid("https://player.vimeo.com/video/552821241")},
        {"title": "Statement of Owner's Equity", "type": "embed", "content": vid("https://player.vimeo.com/video/552821321")},
        {"title": "Classified Balance Sheet for Sole Proprietorships", "type": "embed", "content": vid("https://player.vimeo.com/video/552821390")},
        {"title": "Closing Entries to Retained Earnings", "type": "embed", "content": vid("https://player.vimeo.com/video/552821895")},
        {"title": "Closing Entries to Retained Earning", "type": "embed", "content": vid("https://player.vimeo.com/video/552821758")},
        {"title": "Closing Entries to Retained Earnings", "type": "embed", "content": vid("https://player.vimeo.com/video/552821626")},
        {"title": "Post-Closing Trial Balance for Sole Proprietorships", "type": "embed", "content": vid("https://player.vimeo.com/video/552822062")},
        {"title": "Post-Closing Trial Balance for Corporations", "type": "embed", "content": vid("https://player.vimeo.com/video/552822009")},
        {"title": "Basic Accounting Concepts", "type": "embed", "content": vid("https://player.vimeo.com/video/552826951?quality=720p&audiotrack=main&texttrack=en")},
    ]
)

async def add_lessons():
    course = await db.courses.find_one({"id": "fff9190e-0f7f-483d-b91b-2299013f062c"})
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

    print(f"Added {len(lessons_data)} lessons (131 images + 15 videos)")

if __name__ == "__main__":
    asyncio.run(add_lessons())
