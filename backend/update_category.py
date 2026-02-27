#!/usr/bin/env python3
"""
Script to update category from suply_chain to Supply Chain
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

async def update_category():
    """Update category from suply_chain to Supply Chain"""
    
    result = await db.courses.update_many(
        {"category": "supply_chain"},
        {"$set": {"category": "Supply Chain"}}
    )
    
    print(f"Updated {result.modified_count} courses from 'supply_chain' to 'Supply Chain'")

if __name__ == "__main__":
    asyncio.run(update_category())