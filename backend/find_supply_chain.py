#!/usr/bin/env python3
"""
Script to find diploma in supply chain course
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

async def find_supply_chain_course():
    """Find diploma in supply chain course"""
    
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    if course:
        print(f"Found course: {course['title']}")
        print(f"ID: {course['id']}")
        print(f"Category: {course.get('category', 'N/A')}")
        print(f"Published: {course.get('is_published', False)}")
        print(f"Description: {course.get('description', 'N/A')}")
    else:
        print("Course not found")

if __name__ == "__main__":
    asyncio.run(find_supply_chain_course())