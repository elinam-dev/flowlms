import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

KEEP_PUBLISHED = [
    "cost and management accounting",
    "accounts receive able management",
    "core excel skills",
    "fundamentals of budgeting",
]

async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    finance_courses = await db.courses.find(
        {"category": {"$regex": "finance", "$options": "i"}},
        {"_id": 0, "id": 1, "title": 1, "is_published": 1}
    ).to_list(None)

    print(f"Found {len(finance_courses)} Finance courses\n")

    for course in finance_courses:
        title = course["title"].lower()
        should_keep = any(k in title for k in KEEP_PUBLISHED)

        if should_keep:
            await db.courses.update_one({"id": course["id"]}, {"$set": {"is_published": True}})
            print(f"KEPT:   {course['title']}")
        else:
            await db.courses.update_one({"id": course["id"]}, {"$set": {"is_published": False}})
            print(f"LOCKED: {course['title']}")

    client.close()

if __name__ == "__main__":
    asyncio.run(main())
