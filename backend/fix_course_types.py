#!/usr/bin/env python3
"""
Fix course_type for all courses that have None/missing type.
- Policy courses (HR Policy, Ethics, Safety) = compulsory
- Engineering courses (ENG-*) = compulsory
- Everything else = optional
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def fix_course_types():
    courses = await db.courses.find({}, {'_id': 0, 'id': 1, 'title': 1, 'category': 1, 'code': 1, 'course_type': 1}).to_list(None)

    compulsory_ids = []
    optional_ids = []

    for c in courses:
        code = c.get('code') or ''
        category = c.get('category') or ''
        is_compulsory = (
            code.startswith('ENG-') or
            category in ['HR Policy', 'Ethics', 'Safety'] or
            code in ['LPHR1', 'CEPC3', 'DCPC/HR1', 'H/SP1']
        )
        if is_compulsory:
            compulsory_ids.append(c['id'])
        else:
            optional_ids.append(c['id'])

    # Bulk update compulsory
    r1 = await db.courses.update_many(
        {"id": {"$in": compulsory_ids}},
        {"$set": {"course_type": "compulsory"}}
    )
    # Bulk update optional
    r2 = await db.courses.update_many(
        {"id": {"$in": optional_ids}},
        {"$set": {"course_type": "optional"}}
    )

    print(f"Set {r1.modified_count} courses as compulsory")
    print(f"Set {r2.modified_count} courses as optional")

    # Verify
    comp = await db.courses.count_documents({"course_type": "compulsory"})
    opt = await db.courses.count_documents({"course_type": "optional"})
    print(f"\nVerification: {comp} compulsory, {opt} optional")

if __name__ == "__main__":
    asyncio.run(fix_course_types())
