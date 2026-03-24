import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def check_thumbnails():
    courses = await db.courses.find({"category": "SUPPLY CHAIN"}, {"_id": 0, "title": 1, "thumbnail": 1}).to_list(100)
    
    no_thumbnail = []
    has_thumbnail = []
    
    for course in courses:
        if not course.get("thumbnail") or course.get("thumbnail") == "":
            no_thumbnail.append(course["title"])
        else:
            has_thumbnail.append(course["title"])
    
    print(f"SUPPLY CHAIN COURSES WITHOUT THUMBNAILS: {len(no_thumbnail)}\n")
    for i, title in enumerate(no_thumbnail, 1):
        print(f"{i}. {title}")
    
    print(f"\n\nCOURSES WITH THUMBNAILS: {len(has_thumbnail)}\n")
    for i, title in enumerate(has_thumbnail, 1):
        print(f"{i}. {title}")

if __name__ == "__main__":
    asyncio.run(check_thumbnails())
