#!/usr/bin/env python3
"""
Unpublish all hr and management category courses
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

async def unpublish_hr_courses():
    result = await db.courses.update_many(
        {"category": {"$in": ["hr", "management"]}},
        {"$set": {"is_published": False}}
    )
    print(f"Unpublished {result.modified_count} HR and management courses")

if __name__ == "__main__":
    asyncio.run(unpublish_hr_courses())
