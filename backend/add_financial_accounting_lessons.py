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
    {"title": "Financial Analysis of TCS Limited", "type": "embed", "content": "https://player.vimeo.com/video/908008944?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Effective Tax Rate and Net Profit Margin", "type": "embed", "content": "https://player.vimeo.com/video/908008972?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Current Assets and Current Liability", "type": "embed", "content": "https://player.vimeo.com/video/908008996?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Return on Capital", "type": "embed", "content": "https://player.vimeo.com/video/908009025?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Fundamental Analysis of RIL", "type": "embed", "content": "https://player.vimeo.com/video/908009055?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "RIL ratio Analysis", "type": "embed", "content": "https://player.vimeo.com/video/908009088?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Combined Ratio Analysis", "type": "embed", "content": "https://player.vimeo.com/video/908009122?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Summary of Financial Accounting", "type": "embed", "content": "https://player.vimeo.com/video/908009174?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Summary of Financial Statements", "type": "embed", "content": "https://player.vimeo.com/video/908009211?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Financial Accounting - Slide 21", "type": "text", "content": '<div style="text-align: center;"><img src="http://localhost:8000/uploads/images/Finance/diploma_in_financial_accounting/diploma_in_financial_accounting21.jpeg" alt="Financial Accounting Slide 21" style="max-width: 100%; height: auto;" /></div>'}
]

async def add_lessons():
    # Find course
    course = await db.courses.find_one({"title": {"$regex": "diploma.*financial accounting", "$options": "i"}})
    if not course:
        print("Course not found")
        return
    
    print(f"Found: {course['title']}")
    
    # Find module
    module = await db.modules.find_one({"course_id": course['id']})
    if not module:
        print("Module not found")
        return
    
    # Get current lesson count
    current_lessons = await db.lessons.count_documents({"module_id": module['id']})
    print(f"Current lessons: {current_lessons}")
    
    # Add new lessons
    for i, lesson_data in enumerate(lessons_data):
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module['id'],
            "title": lesson_data['title'],
            "content_type": lesson_data['type'],
            "content": lesson_data['content'],
            "duration_minutes": 10,
            "order": current_lessons + i
        }
        await db.lessons.insert_one(lesson_doc)
    
    print(f"Added {len(lessons_data)} lessons")

if __name__ == "__main__":
    asyncio.run(add_lessons())
