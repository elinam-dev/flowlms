#!/usr/bin/env python3
"""
Upload images to Cloudinary and update database URLs
Install: pip install cloudinary
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

# Cloudinary configuration
# Sign up at https://cloudinary.com for free
# Add these to your .env file:
# CLOUDINARY_CLOUD_NAME=your_cloud_name
# CLOUDINARY_API_KEY=your_api_key
# CLOUDINARY_API_SECRET=your_api_secret

try:
    import cloudinary
    import cloudinary.uploader
    
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False
    print("Cloudinary not installed. Run: pip install cloudinary")

async def upload_to_cloudinary():
    """Upload all supply chain images to Cloudinary"""
    
    if not CLOUDINARY_AVAILABLE:
        print("\nPlease install cloudinary: pip install cloudinary")
        return
    
    images_dir = ROOT_DIR / "uploads" / "images" / "diploma in supply chain"
    
    if not images_dir.exists():
        print(f"Images directory not found: {images_dir}")
        return
    
    # Upload each image
    url_mapping = {}
    for img_file in images_dir.glob("*.jp*g"):
        print(f"Uploading {img_file.name}...")
        try:
            result = cloudinary.uploader.upload(
                str(img_file),
                folder="flowlms/supply-chain",
                public_id=img_file.stem
            )
            url_mapping[img_file.name] = result['secure_url']
            print(f"  ✓ Uploaded: {result['secure_url']}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    # Update database
    print("\nUpdating database...")
    lessons = await db.lessons.find({
        "$or": [
            {"content": {"$regex": "/uploads/images/diploma in supply chain/"}},
            {"content_type": "image"}
        ]
    }).to_list(None)
    
    updated = 0
    for lesson in lessons:
        content = lesson.get("content", "")
        new_content = content
        
        # Replace each image URL
        for filename, cloudinary_url in url_mapping.items():
            old_url = f"/uploads/images/diploma in supply chain/{filename}"
            if old_url in content:
                new_content = new_content.replace(old_url, cloudinary_url)
        
        if new_content != content:
            await db.lessons.update_one(
                {"id": lesson["id"]},
                {"$set": {"content": new_content}}
            )
            print(f"  ✓ Updated: {lesson['title']}")
            updated += 1
    
    print(f"\nDone! Updated {updated} lessons with Cloudinary URLs")

if __name__ == "__main__":
    asyncio.run(upload_to_cloudinary())
