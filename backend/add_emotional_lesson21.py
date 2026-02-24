import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": {"$regex": "Emotional resilience at work", "$options": "i"}})
    modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
    module_id = modules[0]["id"]
    
    image_html = '<div style="text-align: center;"><img src="http://127.0.0.1:8000/api/uploads/images/emotional12.jpeg" alt="Slide 21" style="max-width: 100%; height: auto;" /></div>'
    
    await db.lessons.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module_id,
        "title": "Slide 21",
        "content_type": "text",
        "content": image_html,
        "duration_minutes": 5,
        "order": 20
    })
    
    print("Added lesson 21 with emotional12.jpeg")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
