import asyncio, os, uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE = "http://localhost:8000/uploads/images/Finance/core_excel"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/core_excel{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = [
    {"title": "Core Excel Skills - Slide 1", "type": "text", "content": img(1)},
    {"title": "Introduction", "type": "embed", "content": vid("https://player.vimeo.com/video/476354832?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Logical Tests & Conditional Statements", "type": "embed", "content": vid("https://player.vimeo.com/video/476354869?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "IF Statements", "type": "embed", "content": vid("https://player.vimeo.com/video/476354960?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Sum with Criteria", "type": "embed", "content": vid("https://player.vimeo.com/video/476355490?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "VLOOKUP", "type": "embed", "content": vid("https://player.vimeo.com/video/476355142?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "INDEX and MATCH", "type": "embed", "content": vid("https://player.vimeo.com/video/476355275?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "XLOOKUP", "type": "embed", "content": vid("https://player.vimeo.com/video/476356087?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Working with Tables", "type": "embed", "content": vid("https://player.vimeo.com/video/476355526?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Pivot Table Overview", "type": "embed", "content": vid("https://player.vimeo.com/video/477125807?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Basic Points on Dynamic Arrays", "type": "embed", "content": vid("https://player.vimeo.com/video/477125822?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Dynamic Arrays - Pivot Table Alternatives", "type": "embed", "content": vid("https://player.vimeo.com/video/476355855?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "UNIQUE, SORT and SORTBY", "type": "embed", "content": vid("https://player.vimeo.com/video/477125843?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "The FILTER Function", "type": "embed", "content": vid("https://player.vimeo.com/video/476355913?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Conclusion", "type": "embed", "content": vid("https://player.vimeo.com/video/476356176?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Core Excel Skills - Slide 2", "type": "text", "content": img(2)},
]

async def main():
    course = await db.courses.find_one({"id": "ddafd679-00f1-4b08-bbd2-00246952a4c3"})
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
