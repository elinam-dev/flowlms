"""
Sync enrolled_courses on user documents from enrolled_users on course documents.
Run once: python sync_enrolled_courses.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "flowitec_lms")

async def sync():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    courses = await db.courses.find({}, {"_id": 0, "id": 1, "enrolled_users": 1}).to_list(1000)

    # Build map: user_id -> set of course_ids they're enrolled in
    user_course_map = {}
    for course in courses:
        for user_id in course.get("enrolled_users", []):
            user_course_map.setdefault(user_id, set()).add(course["id"])

    updated = 0
    for user_id, course_ids in user_course_map.items():
        user = await db.users.find_one({"id": user_id}, {"_id": 0, "enrolled_courses": 1})
        if not user:
            continue
        existing = set(user.get("enrolled_courses", []))
        missing = course_ids - existing
        if missing:
            await db.users.update_one(
                {"id": user_id},
                {"$addToSet": {"enrolled_courses": {"$each": list(missing)}}}
            )
            print(f"User {user_id}: added {len(missing)} missing course(s)")
            updated += 1

    print(f"\nDone. Updated {updated} users.")
    client.close()

asyncio.run(sync())
