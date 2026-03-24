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

new_lessons = [
    {"title": "Working With Advanced VLOOKUP", "type": "embed", "content": vid("https://player.vimeo.com/video/907949667?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "HLOOKUP–INDEX–MATCH Functions", "type": "embed", "content": vid("https://player.vimeo.com/video/907949713?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Modifying Existing Templates", "type": "embed", "content": vid("https://player.vimeo.com/video/907949754?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Copying Macros Between Workbooks", "type": "embed", "content": vid("https://player.vimeo.com/video/907949791?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Working With External Data Sources", "type": "embed", "content": vid("https://player.vimeo.com/video/907949824?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Exploring Tracking Changes Feature", "type": "embed", "content": vid("https://player.vimeo.com/video/907949850?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Course Conclusion", "type": "embed", "content": vid("https://player.vimeo.com/video/907949884?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Top 25 Excel Formulas - Slide 7", "type": "text", "content": img(7)},
    {"title": "Top 25 Excel Formulas - Slide 8", "type": "text", "content": img(8)},
    {"title": "Top 25 Excel Formulas - Slide 9", "type": "text", "content": img(9)},
]

async def main():
    course = await db.courses.find_one({"id": "579d9692-fbb2-4193-8994-4d41a3298535"})
    module = await db.modules.find_one({"course_id": course["id"]})
    count = await db.lessons.count_documents({"module_id": module["id"]})
    for i, lesson in enumerate(new_lessons):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson["title"],
            "content_type": lesson["type"],
            "content": lesson["content"],
            "duration_minutes": 10,
            "order": count + i
        })
    print(f"Added {len(new_lessons)} lessons. Total: {count + len(new_lessons)}")

asyncio.run(main())
