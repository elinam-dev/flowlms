#!/usr/bin/env python3
"""
Make the 4 engineering courses available to every user:
1. Set course_type to 'compulsory' so new users get auto-enrolled
2. Enroll all existing learners who aren't already enrolled
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

ENG_CODES = ['ENG-PUMP-002', 'ENG-PUMP-003', 'ENG-PUMP-004', 'ENG-VALVE-001']

async def assign_engineering_courses():
    # Find the 4 engineering courses
    courses = await db.courses.find({"code": {"$in": ENG_CODES}}, {"_id": 0}).to_list(None)
    if not courses:
        print("Engineering courses not found by code, trying by title...")
        courses = await db.courses.find({
            "title": {"$regex": "pump|valve", "$options": "i"},
            "code": {"$regex": "ENG", "$options": "i"}
        }, {"_id": 0}).to_list(None)

    print(f"Found {len(courses)} engineering courses:")
    for c in courses:
        print(f"  - {c['title']} ({c.get('code','no code')})")

    # Set all 4 as compulsory
    for course in courses:
        await db.courses.update_one(
            {"_id": (await db.courses.find_one({"id": course["id"]}))["_id"]},
            {"$set": {"course_type": "compulsory"}}
        )
    print("\nSet all 4 as compulsory")

    # Get all users
    users = await db.users.find({}, {"_id": 0, "id": 1, "role": 1, "enrolled_courses": 1}).to_list(None)
    print(f"\nProcessing {len(users)} users...")

    enrolled_count = 0
    for user in users:
        user_enrolled = user.get("enrolled_courses", [])
        for course in courses:
            if course["id"] in user_enrolled:
                continue
            # Enroll user
            await db.users.update_one(
                {"id": user["id"]},
                {"$addToSet": {"enrolled_courses": course["id"]}}
            )
            await db.courses.update_one(
                {"id": course["id"]},
                {"$addToSet": {"enrolled_users": user["id"]}}
            )
            # Init progress
            await db.progress.insert_one({
                "id": str(uuid.uuid4()),
                "user_id": user["id"],
                "course_id": course["id"],
                "completed_lessons": [],
                "quiz_scores": {},
                "percentage": 0,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "last_accessed": datetime.now(timezone.utc).isoformat()
            })
            enrolled_count += 1

    print(f"Enrolled {enrolled_count} user-course pairs")
    print("\nDone! All users now have the 4 engineering courses.")

if __name__ == "__main__":
    asyncio.run(assign_engineering_courses())
