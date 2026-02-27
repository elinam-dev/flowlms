#!/usr/bin/env python3
"""
Script to update Incoterms image paths for Vercel deployment
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

async def update_incoterms_images():
    """Update Incoterms images to use external URLs"""
    
    # Update course thumbnail
    await db.courses.update_one(
        {"title": {"$regex": "incoterms", "$options": "i"}},
        {"$set": {"thumbnail": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=400&h=225&fit=crop"}}
    )
    
    # Update lesson images to use placeholder or external URLs
    base_url = "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&h=600&fit=crop&q=80"
    
    lessons = await db.lessons.find({"content": {"$regex": "/api/uploads/images/incoterms"}}).to_list(1000)
    
    for lesson in lessons:
        # Replace local image paths with external URL
        updated_content = lesson["content"].replace(
            'src="/api/uploads/images/incoterms/',
            f'src="{base_url}&sig='
        ).replace('.jpeg"', '"')
        
        await db.lessons.update_one(
            {"id": lesson["id"]},
            {"$set": {"content": updated_content}}
        )
    
    print(f"Updated {len(lessons)} lessons with external image URLs")

if __name__ == "__main__":
    asyncio.run(update_incoterms_images())