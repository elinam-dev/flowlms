#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def unpublish():
    result = await db.courses.update_one(
        {"title": {"$regex": "diploma.*supply.*chain", "$options": "i"}},
        {"$set": {"is_published": False}}
    )
    if result.matched_count:
        print("Diploma in Supply Chain Management has been taken down (unpublished).")
    else:
        print("Course not found.")

if __name__ == "__main__":
    asyncio.run(unpublish())
