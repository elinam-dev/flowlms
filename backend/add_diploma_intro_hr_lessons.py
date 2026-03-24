import asyncio, os, uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = [
    {"title": "Topic 1", "content": vid("https://player.vimeo.com/video/1094766683?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Topic 2", "content": vid("https://player.vimeo.com/video/1094766776?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Topic 3", "content": vid("https://player.vimeo.com/video/1094766832?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Topic 4", "content": vid("https://player.vimeo.com/video/1094766967?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Topic 5", "content": vid("https://player.vimeo.com/video/1094767123?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Topic 6", "content": vid("https://player.vimeo.com/video/1094767226?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Topic 7", "content": vid("https://player.vimeo.com/video/1094767362?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Topic 8", "content": vid("https://player.vimeo.com/video/1094767362?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Topic 9", "content": vid("https://player.vimeo.com/video/1094767524?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Topic 10", "content": vid("https://player.vimeo.com/video/1094767628?quality=720p&audiotrack=main&texttrack=en")},
]

async def main():
    course = await db.courses.find_one({"id": "aae026b3-567e-4078-9fc3-1fe9cbde2b92"})
    print(f"Course: {course['title']}")
    module = await db.modules.find_one({"course_id": course["id"]})
    await db.lessons.delete_many({"module_id": module["id"]})
    for i, lesson in enumerate(lessons_data):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson["title"],
            "content_type": "embed",
            "content": lesson["content"],
            "duration_minutes": 10,
            "order": i
        })
    print(f"Added {len(lessons_data)} lessons")

asyncio.run(main())
