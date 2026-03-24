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

video_urls = [
    "https://player.vimeo.com/video/1094603537?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094603567?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094603595?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094603630?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094603666?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094603694?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094603751?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094603798?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094603845?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094603876?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094603928?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604007?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604044?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604076?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604111?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604202?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604282?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604332?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604369?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604418?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604446?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604488?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604532?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604587?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604616?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604657?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604726?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604782?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094604814?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094707932?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094708005?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094708057?quality=720p&audiotrack=main&texttrack=en",
    "https://player.vimeo.com/video/1094708104?quality=720p&audiotrack=main&texttrack=en"
]

async def add_lessons():
    # Find course
    course = await db.courses.find_one({"id": "30aa996f-32d1-49f9-9829-616d157ea438"})
    
    # Find module
    module = await db.modules.find_one({"course_id": course['id']})
    
    # Delete existing lesson
    await db.lessons.delete_many({"module_id": module['id']})
    
    # Add new lessons
    for i, url in enumerate(video_urls):
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module['id'],
            "title": f"Business Accounting - Lesson {i+1}",
            "content_type": "embed",
            "content": url,
            "duration_minutes": 10,
            "order": i
        }
        await db.lessons.insert_one(lesson_doc)
    
    print(f"Added {len(video_urls)} video lessons to {course['title']}")

if __name__ == "__main__":
    asyncio.run(add_lessons())