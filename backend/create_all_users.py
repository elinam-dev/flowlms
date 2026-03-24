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
    {"first_name": "Ali",        "last_name": "Issahak",       "employee_id": "FF10011",   "department": "finance",      "password": "Ali@Ff2025"},
    {"first_name": "Francisca",  "last_name": "Cudjoe",        "employee_id": "FF10012",   "department": "finance",      "password": "Fran@Ff2025"},
    {"first_name": "Diana",      "last_name": "Awuni",         "employee_id": "FCGH10013", "department": "supply_chain", "password": "Diana@Fc2025"},
    {"first_name": "Jonas",      "last_name": "Sedzro",        "employee_id": "FCGH10014", "department": "supply_chain", "password": "Jonas@Fc2025"},
    {"first_name": "Salome",     "last_name": "Ndego",         "employee_id": "FCGH10015", "department": "supply_chain", "password": "Salom@Fc2025"},
    {"first_name": "Vivian",     "last_name": "Dodoo",         "employee_id": "FCGH10016", "department": "supply_chain", "password": "Vivian@Fc2025"},
    {"first_name": "Nathan",     "last_name": "Nshiah",        "employee_id": "FCNS10017", "department": "supply_chain", "password": "Nathan@Fc2025"},
    {"first_name": "Roger",      "last_name": "Owusu",         "employee_id": "FCNS10018", "department": "supply_chain", "password": "Roger@Fc2025"},
    {"first_name": "Joseph",     "last_name": "Igbama Osas",   "employee_id": "FCNG10019", "department": "supply_chain", "password": "Joseph@Fc2025"},
    {"first_name": "Thank God",  "last_name": "Songu",         "employee_id": "FSGH10021", "department": "sales",        "password": "TGod@Fs2025"},
    {"first_name": "Angelo",     "last_name": "Apedo-Pedro",   "employee_id": "FSNS10022", "department": "sales",        "password": "Angel@Fs2025"},
    {"first_name": "Gabriel",    "last_name": "Ampofo",        "employee_id": "FSNS10023", "department": "sales",        "password": "Gabri@Fs2025"},
    {"first_name": "Lynette",    "last_name": "Djanie",        "employee_id": "FSGH10024", "department": "sales",        "password": "Lynet@Fs2025"},
    {"first_name": "John",       "last_name": "Dada",          "employee_id": "FSNG10025", "department": "sales",        "password": "John@Fs2025"},
    {"first_name": "Winnie",     "last_name": "Mwangi",        "employee_id": "FSKN10026", "department": "sales",        "password": "Winni@Fs2025"},
    {"first_name": "Peter",      "last_name": "Muinde",        "employee_id": "FSKN10027", "department": "sales",        "password": "Peter@Fs2025"},
    {"first_name": "Patience",   "last_name": "Dzisenu",       "employee_id": "FHGH10027", "department": "hr",           "password": "Patie@Fh2025", "role": "admin"},
    {"first_name": "Mayfred",    "last_name": "Gyamfua Owusu", "employee_id": "FHGH10028", "department": "hr",           "password": "Mayfd@Fh2025"},
    {"first_name": "Judith",     "last_name": "Anang-Isaacs",  "employee_id": "FHGH10029", "department": "hr",           "password": "Judit@Fh2025"},
    {"first_name": "Titilope",   "last_name": "Abimbola",      "employee_id": "FHNG10031", "department": "hr",           "password": "Titil@Fh2025"},
    {"first_name": "Issabel",    "last_name": "Ofori",         "employee_id": "FE10032",   "department": "general",      "password": "Issa@Fe2025"},
]

async def main():
    compulsory_courses = await db.courses.find(
        {"course_type": "compulsory", "is_published": True}, {"_id": 0, "id": 1}
    ).to_list(100)
    compulsory_ids = [c["id"] for c in compulsory_courses]

    for u in users:
        email = f"{u['first_name'].lower().replace(' ', '.')}.{u['last_name'].lower().replace(' ', '.').replace('-', '')}@flowitec.com"

        # Check by employee_id or email
        existing = await db.users.find_one({"$or": [{"employee_id": u["employee_id"]}, {"email": email}]})
        if existing:
            if existing.get("employee_id") != u["employee_id"]:
                await db.users.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {"employee_id": u["employee_id"], "department": u["department"]}}
                )
                print(f"UPDATED: {existing.get('employee_id')} -> {u['employee_id']} | {u['first_name']} {u['last_name']}")
            else:
                print(f"SKIP: {u['employee_id']} | {u['first_name']} {u['last_name']} already exists")
            continue

        user_id = str(uuid.uuid4())
        user_doc = {
            "id": user_id,
            "email": email,
            "password": hash_password(u["password"]),
            "first_name": u["first_name"],
            "last_name": u["last_name"],
            "employee_id": u["employee_id"],
            "department": u["department"],
            "role": u.get("role", "learner"),
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
