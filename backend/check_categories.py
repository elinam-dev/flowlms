#!/usr/bin/env python3
"""
Script to check existing categories
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

async def check_categories():
    """Check existing categories"""
    
    categories = await db.courses.distinct("category")
    print("Existing categories:")
    for cat in categories:
        print(f"  - {cat}")

if __name__ == "__main__":
    asyncio.run(check_categories())