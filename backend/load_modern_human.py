import asyncio
import uuid
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "https://flowlms-production.up.railway.app")
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

SLIDES_FOLDER = r"c:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\HR\modern_human"

async def main():
    course = await db.courses.find_one(
        {'title': {'$regex': 'Recruitment and selection', '$options': 'i'}},
        {'_id': 0}
    )
    course_id = course['id']
    print(f"Course: {course['title']} ({course_id})")

    old_modules = await db.modules.find({'course_id': course_id}, {'_id': 0, 'id': 1}).to_list(100)
    for m in old_modules:
        await db.lessons.delete_many({'module_id': m['id']})
    await db.modules.delete_many({'course_id': course_id})
    print("Cleared old module/lessons")

    module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        'id': module_id,
        'course_id': course_id,
        'title': 'Modern HRM - Recruitment and Selection Process',
        'description': 'Course slides for Modern Human Resource Management - Recruitment and Selection',
        'order': 1,
    })

    files = sorted([f for f in os.listdir(SLIDES_FOLDER) if f.endswith('.jpeg')])
    print(f"Loading {len(files)} slides...")

    lessons = []
    for i, filename in enumerate(files, start=1):
        img_url = f"{BACKEND_URL}/api/uploads/images/HR/modern_human/{filename}"
        lessons.append({
            'id': str(uuid.uuid4()),
            'module_id': module_id,
            'title': f'Slide {i}',
            'content_type': 'text',
            'content': f'<div style="text-align: center;"><img src="{img_url}" alt="Slide {i}" style="max-width: 100%; height: auto;" /></div>',
            'duration_minutes': 2,
            'order': i,
            'created_at': datetime.now(timezone.utc).isoformat(),
        })

    await db.lessons.insert_many(lessons)
    await db.courses.update_one(
        {'id': course_id},
        {'$set': {'published': True, 'is_published': True}}
    )

    print(f"Done! Inserted {len(lessons)} lessons and published the course.")

asyncio.run(main())
