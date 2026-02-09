"""
Run this script to seed all 17 SALES courses
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from seed_sales_courses_full import seed_sales_courses

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def main():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Starting to seed 17 SALES courses...")
    await seed_sales_courses(db)
    print("Seeding complete!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
