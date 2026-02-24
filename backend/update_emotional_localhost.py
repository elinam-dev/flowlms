import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def update():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": {"$regex": "Emotional resilience at work", "$options": "i"}})
    modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
    module_id = modules[0]["id"]
    
    lessons = await db.lessons.find({"module_id": module_id}).sort("order", 1).to_list(100)
    lesson = lessons[0]
    
    image_html = '<div style="text-align: center;"><img src="http://127.0.0.1:8000/api/uploads/images/emotional.jpeg" alt="Emotional Resilience" style="max-width: 100%; height: auto;" /></div>'
    
    await db.lessons.update_one(
        {"id": lesson["id"]},
        {"$set": {"content": image_html}}
    )
    
    print("Updated to localhost URL")
    client.close()

if __name__ == "__main__":
    asyncio.run(update())
