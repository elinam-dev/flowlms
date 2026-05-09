#!/usr/bin/env python3
"""
Create Employee Handbook Final Word course:
- compulsory (visible to all staff)
- 34 page lessons from employee_handbook folder
- Enroll all existing users
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE_URL = "https://flowlms-production.up.railway.app"
IMG_DIR = ROOT_DIR / "uploads" / "images" / "employee_handbook"

async def setup():
    # Get images sorted by name
    files = sorted([f for f in IMG_DIR.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg']])
    print(f"Found {len(files)} images")

    # Create course
    existing = await db.courses.find_one({'title': {'$regex': 'employee handbook final', '$options': 'i'}})
    if existing:
        await db.courses.delete_one({'_id': existing['_id']})
        modules = await db.modules.find({'course_id': existing['id']}).to_list(None)
        module_ids = [m['id'] for m in modules]
        await db.lessons.delete_many({'module_id': {'$in': module_ids}})
        await db.modules.delete_many({'course_id': existing['id']})

    course_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": course_id,
        "title": "Employee Handbook Final Word",
        "description": "The official Flowitec Employee Handbook covering all company policies, procedures, and guidelines that every employee must read and understand.",
        "category": "HR Policy",
        "course_type": "compulsory",
        "duration_hours": 2,
        "is_published": True,
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    print("Created course")

    # Create module
    module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": module_id,
        "course_id": course_id,
        "title": "Course Content",
        "order": 0
    })

    # Add lessons
    for i, f in enumerate(files):
        url = f"{BASE_URL}/uploads/images/employee_handbook/{f.name}"
        content = f'<div style="text-align: center; padding: 20px;"><img src="{url}" alt="Page {i+1}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": f"Page {i+1}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 3,
            "order": i
        })

    print(f"Added {len(files)} lessons")

    # Enroll all users and add to course enrolled_users
    users = await db.users.find({}, {'_id': 0, 'id': 1, 'enrolled_courses': 1}).to_list(None)
    enrolled_count = 0
    for user in users:
        if course_id not in user.get('enrolled_courses', []):
            await db.users.update_one({'id': user['id']}, {'$addToSet': {'enrolled_courses': course_id}})
            await db.courses.update_one({'id': course_id}, {'$addToSet': {'enrolled_users': user['id']}})
            await db.progress.insert_one({
                "id": str(uuid.uuid4()),
                "user_id": user['id'],
                "course_id": course_id,
                "completed_lessons": [],
                "quiz_scores": {},
                "percentage": 0,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "last_accessed": datetime.now(timezone.utc).isoformat()
            })
            enrolled_count += 1

    print(f"Enrolled {enrolled_count} users")
    print("Done! Course is published and compulsory.")

if __name__ == "__main__":
    asyncio.run(setup())
