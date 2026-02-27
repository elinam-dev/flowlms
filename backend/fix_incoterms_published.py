import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def fix_incoterms():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Update Incoterms course to be published
    result = await db.courses.update_one(
        {"id": "incoterms_2024"},
        {"$set": {"is_published": True}}
    )
    
    print(f"Updated {result.modified_count} course(s)")
    
    # Verify the update
    course = await db.courses.find_one({"id": "incoterms_2024"})
    if course:
        print(f"\nIncoterms course status:")
        print(f"Title: {course.get('title')}")
        print(f"Published: {course.get('is_published')}")
        print(f"Category: {course.get('category')}")
    
    client.close()

if __name__ == '__main__':
    asyncio.run(fix_incoterms())
