import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"code": "ENG-VALVE-001"})
    module = await db.modules.find_one({"course_id": course["id"]})
    lessons = await db.lessons.find({"module_id": module["id"]}).to_list(100)
    
    for i, lesson in enumerate(lessons, 1):
        new_content = f'<div style="text-align: center;"><img src="http://127.0.0.1:8000/api/uploads/images/valve_{i:02d}.png" alt="Slide {i}" style="max-width: 100%; height: auto;" /></div>'
        await db.lessons.update_one(
            {"id": lesson["id"]},
            {"$set": {"content": new_content}}
        )
    
    await db.courses.update_one(
        {"code": "ENG-VALVE-001"},
        {"$set": {"thumbnail": "http://127.0.0.1:8000/api/uploads/images/valve_01.png"}}
    )
    
    print(f"Updated {len(lessons)} lessons")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
