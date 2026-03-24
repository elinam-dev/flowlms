#!/usr/bin/env python3
"""
Fix lesson order for Diploma in Supply Chain Management.
Correct order based on module structure:
1.  The SCOR Model Framework
2.  The Bullwhip Effect (+ supplychain2.jpg)
3.  The Kraljic Matrix
4.  Total Cost of Ownership (TCO) (+ supplychain3.jpg)
5.  The Economic Order Quantity (EOQ) (+ supplychain4.jpg)
6.  Warehouse Design: The Honeycombing Effect
7.  Incoterms 2020 (new)
8.  The Last Mile & Cold Chain
9.  Industry 4.0 Technologies
10. Risk Management: The FMEA Framework (+ supplychain5.jpg)
11. The Cash-to-Cash (C2C) Conversion Cycle (+ supplychain6.jpg)
"""
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

# Correct title order for lessons 1-11 (0-indexed order values 0-10)
CORRECT_ORDER = [
    "The SCOR Model Framework",
    "The Bullwhip Effect: Mathematics of Distortion",
    "The Kraljic Matrix",
    "Total Cost of Ownership (TCO)",
    "The Economic Order Quantity (EOQ)",
    "Warehouse Design: The Honeycombing Effect",
    "The Last Mile & Cold Chain",
    "Industry 4.0 Technologies",
    "Risk Management: The FMEA Framework",
    "The Cash-to-Cash (C2C) Conversion Cycle",
    "Supply Chain Financing (SCF)",
]

async def fix_order():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    if not course:
        print("Course not found!")
        return

    # Collect all lessons across all modules
    modules = await db.modules.find({"course_id": course["id"]}).to_list(None)
    all_lessons = []
    for module in modules:
        lessons = await db.lessons.find({"module_id": module["id"]}).to_list(None)
        all_lessons.extend(lessons)

    # Build a title -> lesson map
    lesson_map = {l["title"]: l for l in all_lessons}

    # Assign correct order values 0-10 for the first 11 lessons
    updated = 0
    for new_order, title in enumerate(CORRECT_ORDER):
        lesson = lesson_map.get(title)
        if not lesson:
            print(f"  WARNING: Lesson not found: '{title}'")
            continue
        await db.lessons.update_one(
            {"id": lesson["id"]},
            {"$set": {"order": new_order}}
        )
        print(f"  [{new_order}] {title}")
        updated += 1

    # Push all other lessons to order 100+ so they don't interfere
    for lesson in all_lessons:
        if lesson["title"] not in CORRECT_ORDER:
            current_order = lesson.get("order", 0)
            if current_order < 100:
                await db.lessons.update_one(
                    {"id": lesson["id"]},
                    {"$set": {"order": current_order + 100}}
                )

    print(f"\nDone! Reordered {updated} lessons.")

if __name__ == "__main__":
    asyncio.run(fix_order())
