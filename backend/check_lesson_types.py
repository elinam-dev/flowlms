import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

async def main():
    # Get distinct content types
    types = await db.lessons.distinct('content_type')
    print("Content types:", types)
    
    # Get a sample of each
    for t in types:
        lesson = await db.lessons.find_one({'content_type': t}, {'_id': 0, 'title': 1, 'content_type': 1, 'content': 1})
        print(f"\n--- {t} ---")
        content = str(lesson.get('content', ''))[:200]
        print(f"Title: {lesson.get('title')}")
        print(f"Content preview: {content}")

asyncio.run(main())
