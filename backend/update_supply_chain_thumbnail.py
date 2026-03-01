#!/usr/bin/env python3
"""
Script to update supply chain course thumbnail
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

async def update_supply_chain_thumbnail():
    """Update supply chain course thumbnail"""
    
    result = await db.courses.update_one(
        {"title": {"$regex": "diploma.*supply.*chain", "$options": "i"}},
        {"$set": {"thumbnail": "https://flowlms-production.up.railway.app/api/uploads/images/diploma in supply chain/supplychain1.jpeg"}}
    )
    
    if result.modified_count > 0:
        print("Updated supply chain course thumbnail")
    else:
        print("No changes made")

if __name__ == "__main__":
    asyncio.run(update_supply_chain_thumbnail())