#!/usr/bin/env python3
"""
Script to update Incoterms course thumbnail
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def update_incoterms_thumbnail():
    """Update Incoterms course thumbnail"""
    
    # Find Incoterms course
    course = await db.courses.find_one({"title": {"$regex": "incoterms", "$options": "i"}})
    
    if not course:
        print("Incoterms course not found")
        return
    
    # Update thumbnail
    result = await db.courses.update_one(
        {"id": course["id"]},
        {"$set": {"thumbnail": "/api/uploads/images/incoterms.jpeg"}}
    )
    
    if result.modified_count > 0:
        print(f"Updated thumbnail for course: {course['title']}")
    else:
        print("No changes made")

if __name__ == "__main__":
    asyncio.run(update_incoterms_thumbnail())