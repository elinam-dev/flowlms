import asyncio, os, uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone
import bcrypt

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

users = [
    {"first_name": "Ali", "last_name": "Issahak", "employee_id": "FF10011", "department": "finance", "password": "Ali@Ff2025"},
    {"first_name": "Francisca", "last_name": "Cudjoe", "employee_id": "FF10012", "department": "finance", "password": "Fran@Ff2025"},
    {"first_name": "Diana", "last_name": "Awuni", "employee_id": "FC10013", "department": "supply_chain", "password": "Diana@Fc2025"},
    {"first_name": "Jonas", "last_name": "Sedzro", "employee_id": "FC10014", "department": "supply_chain", "password": "Jonas@Fc2025"},
    {"first_name": "Salome", "last_name": "Ndego", "employee_id": "FC10015", "department": "supply_chain", "password": "Salom@Fc2025"},
]

async def main():
    compulsory_courses = await db.courses.find(
        {"course_type": "compulsory", "is_published": True}, {"_id": 0, "id": 1}
    ).to_list(100)
    compulsory_ids = [c["id"] for c in compulsory_courses]

    for u in users:
        existing = await db.users.find_one({"employee_id": u["employee_id"]})
        if existing:
            print(f"SKIP: {u['employee_id']} already exists")
            continue

        user_id = str(uuid.uuid4())
        email = f"{u['first_name'].lower()}.{u['last_name'].lower()}@flowitec.com"
        user_doc = {
            "id": user_id,
            "email": email,
            "password": hash_password(u["password"]),
            "first_name": u["first_name"],
            "last_name": u["last_name"],
            "employee_id": u["employee_id"],
            "department": u["department"],
            "role": "learner",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "enrolled_courses": compulsory_ids,
            "completed_courses": [],
            "certificates": [],
            "check_ins": [],
            "streak": 0,
            "last_check_in": None
        }
        await db.users.insert_one(user_doc)

        for course_id in compulsory_ids:
            await db.courses.update_one({"id": course_id}, {"$addToSet": {"enrolled_users": user_id}})
            await db.progress.insert_one({
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "course_id": course_id,
                "completed_lessons": [],
                "quiz_scores": {},
                "percentage": 0,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "last_accessed": datetime.now(timezone.utc).isoformat()
            })

        print(f"Created: {u['first_name']} {u['last_name']} | ID: {u['employee_id']} | Password: {u['password']}")

asyncio.run(main())
