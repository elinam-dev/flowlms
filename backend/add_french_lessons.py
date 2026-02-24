import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": {"$regex": "french", "$options": "i"}})
    modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
    module_id = modules[0]["id"]
    
    # Delete existing lesson
    await db.lessons.delete_many({"module_id": module_id})
    
    # Add 286 lessons
    for i in range(1, 287):
        image_html = f'<div style="text-align: center;"><img src="http://127.0.0.1:8000/api/uploads/images/french/complete_french_page-{i:04d}.jpg" alt="Page {i}" style="max-width: 100%; height: auto;" /></div>'
        
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": f"Page {i}",
            "content_type": "text",
            "content": image_html,
            "duration_minutes": 3,
            "order": i - 1
        })
        
        if i % 50 == 0:
            print(f"Added {i} lessons...")
    
    print(f"Added all 286 French lessons")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
