import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def clear():
    # Clear enrolled_courses on all users
    r1 = await db.users.update_many({}, {"$set": {"enrolled_courses": [], "completed_courses": [], "certificates": []}})
    print(f"Cleared enrollments for {r1.modified_count} users")

    # Clear enrolled_users on all courses
    r2 = await db.courses.update_many({}, {"$set": {"enrolled_users": []}})
    print(f"Cleared enrolled_users on {r2.modified_count} courses")

    # Delete all progress records
    r3 = await db.progress.delete_many({})
    print(f"Deleted {r3.deleted_count} progress records")

    print("Done.")
    client.close()

asyncio.run(clear())
