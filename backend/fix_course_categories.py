import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def fix():
    # Fix Engineering courses with no course_type
    r1 = await db.courses.update_many(
        {"category": "Engineering", "course_type": None},
        {"$set": {"course_type": "optional", "is_published": True}}
    )
    print(f"Fixed Engineering course_type: {r1.modified_count}")

    # Fix Incoterms course_type
    r2 = await db.courses.update_many(
        {"category": "Supply Chain", "course_type": None},
        {"$set": {"course_type": "optional", "is_published": True}}
    )
    print(f"Fixed Supply Chain course_type: {r2.modified_count}")

    # Fix 'general' category HR courses -> move to 'hr'
    r3 = await db.courses.update_many(
        {"category": "general"},
        {"$set": {"category": "hr"}}
    )
    print(f"Moved general -> hr: {r3.modified_count}")

    print("Done.")
    client.close()

asyncio.run(fix())
