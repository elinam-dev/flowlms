"""
Update course thumbnails with category-specific images
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Category-specific image mappings using Unsplash
CATEGORY_IMAGES = {
    "HR Policy": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=450&fit=crop",
    "Ethics": "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=800&h=450&fit=crop",
    "Safety": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=800&h=450&fit=crop",
    "SALES (ENGINEER)": "https://images.unsplash.com/photo-1556761175-b413da4baf72?w=800&h=450&fit=crop",
    "SUPPLY CHAIN": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&h=450&fit=crop",
    "FINANCE": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=800&h=450&fit=crop",
    "HUMAN RESOURCES": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800&h=450&fit=crop",
    "MANAGEMENT": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=800&h=450&fit=crop",
    "ENGINEERING": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=800&h=450&fit=crop",
    "HEALTH & SAFETY": "https://images.unsplash.com/photo-1584515933487-779824d29309?w=800&h=450&fit=crop",
    "PERSONAL DEVELOPMENT": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=450&fit=crop",
    "LANGUAGE": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=800&h=450&fit=crop"
}

async def update_thumbnails():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Updating course thumbnails...")
    
    courses = await db.courses.find({}).to_list(1000)
    updated_count = 0
    
    for course in courses:
        category = course.get('category', 'PERSONAL DEVELOPMENT')
        thumbnail = CATEGORY_IMAGES.get(category, CATEGORY_IMAGES['PERSONAL DEVELOPMENT'])
        
        await db.courses.update_one(
            {"id": course["id"]},
            {"$set": {"thumbnail": thumbnail}}
        )
        
        updated_count += 1
        print(f"  ✓ {course['title']}: {category}")
    
    print(f"\n✅ Updated {updated_count} course thumbnails!")
    client.close()

if __name__ == "__main__":
    asyncio.run(update_thumbnails())
