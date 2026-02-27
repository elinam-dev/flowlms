#!/usr/bin/env python3
"""
Script to unenroll all users from all courses
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

async def unenroll_all_users():
    """Unenroll all users from all courses"""
    
    print("Unenrolling all users from all courses...")
    
    # Clear enrolled_users from all courses
    courses_result = await db.courses.update_many(
        {},
        {"$set": {"enrolled_users": []}}
    )
    print(f"Updated {courses_result.modified_count} courses")
    
    # Clear enrolled_courses from all users
    users_result = await db.users.update_many(
        {},
        {"$set": {"enrolled_courses": []}}
    )
    print(f"Updated {users_result.modified_count} users")
    
    # Delete all progress records
    progress_result = await db.progress.delete_many({})
    print(f"Deleted {progress_result.deleted_count} progress records")
    
    # Delete all certificates
    cert_result = await db.certificates.delete_many({})
    print(f"Deleted {cert_result.deleted_count} certificates")
    
    print("All users have been unenrolled from all courses!")

if __name__ == "__main__":
    asyncio.run(unenroll_all_users())