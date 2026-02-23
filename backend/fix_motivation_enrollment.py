import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
from datetime import datetime, timezone

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    
    # Find your user (assuming test learner)
    user = await db.users.find_one({"employee_id": "EMP-TEST-01"})
    
    if not user:
        print("User not found")
        return
    
    # Check if already enrolled
    if course["id"] not in user.get("enrolled_courses", []):
        # Add to enrolled courses
        await db.users.update_one(
            {"id": user["id"]},
            {"$push": {"enrolled_courses": course["id"]}}
        )
        await db.courses.update_one(
            {"id": course["id"]},
            {"$push": {"enrolled_users": user["id"]}}
        )
    
    # Create fresh progress
    progress_doc = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "course_id": course["id"],
        "completed_lessons": [],
        "quiz_scores": {},
        "percentage": 0,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "last_accessed": datetime.now(timezone.utc).isoformat()
    }
    await db.progress.insert_one(progress_doc)
    
    print("Fixed enrollment and progress")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
