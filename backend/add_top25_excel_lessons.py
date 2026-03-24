import asyncio, os, uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE = "http://localhost:8000/uploads/images/Finance/top_25_excel_formulas"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/top_25_excel_formulas{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = [
    {"title": "Top 25 Excel Formulas - Slide 1", "type": "text", "content": img(1)},
    {"title": "Introduction", "type": "embed", "content": vid("https://player.vimeo.com/video/907949268?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "What Will I Learn?", "type": "embed", "content": vid("https://player.vimeo.com/video/907949303?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "AND and IF Functions", "type": "embed", "content": vid("https://player.vimeo.com/video/907949329?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "IFERROR and XOR Functions", "type": "embed", "content": vid("https://player.vimeo.com/video/907949371?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "PV and FV Functions", "type": "embed", "content": vid("https://player.vimeo.com/video/907949411?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "PMT–PPMT–PRICE–YIELD Functions", "type": "embed", "content": vid("https://player.vimeo.com/video/907949447?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "PRICE–COUPONDAYS–ACCRINTM Functions", "type": "embed", "content": vid("https://player.vimeo.com/video/907949486?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Depreciation Lecture", "type": "embed", "content": vid("https://player.vimeo.com/video/907949538?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Top 25 Excel Formulas - Slide 2", "type": "text", "content": img(2)},
    {"title": "Top 25 Excel Formulas - Slide 3", "type": "text", "content": img(3)},
    {"title": "Top 25 Excel Formulas - Slide 4", "type": "text", "content": img(4)},
    {"title": "Top 25 Excel Formulas - Slide 5", "type": "text", "content": img(5)},
    {"title": "Top 25 Excel Formulas - Slide 6", "type": "text", "content": img(6)},
    {"title": "TEXT and CONCATENATION Functions", "type": "embed", "content": vid("https://player.vimeo.com/video/907949572?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "PROPER-UPPER-LOWER-SUBSTITUTE Functions", "type": "embed", "content": vid("https://player.vimeo.com/video/907949596?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "LOOKUP Functions Lecture", "type": "embed", "content": vid("https://player.vimeo.com/video/907949637?quality=720p&audiotrack=main&texttrack=en")},
]

async def main():
    course = await db.courses.find_one({"id": "579d9692-fbb2-4193-8994-4d41a3298535"})
    print(f"Course: {course['title']}")
    module = await db.modules.find_one({"course_id": course["id"]})
    await db.lessons.delete_many({"module_id": module["id"]})
    for i, lesson in enumerate(lessons_data):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson["title"],
            "content_type": lesson["type"],
            "content": lesson["content"],
            "duration_minutes": 10,
            "order": i
        })
    print(f"Added {len(lessons_data)} lessons")

asyncio.run(main())
