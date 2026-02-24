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
    
    lessons = [
        {"type": "video", "title": "The Information in Emotions", "video_id": "576740124", "order": 49},
        {"type": "image", "title": "Slide 51", "image": "emotional20.jpeg", "order": 50},
        {"type": "image", "title": "Slide 52", "image": "emotional21.jpeg", "order": 51},
        {"type": "image", "title": "Slide 53", "image": "emotional22.jpeg", "order": 52}
    ]
    
    for lesson in lessons:
        if lesson["type"] == "video":
            content = f'''<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
    <iframe src="https://player.vimeo.com/video/{lesson["video_id"]}?quality=720p&audiotrack=main&texttrack=en" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
            frameborder="0" 
            allow="autoplay; fullscreen; picture-in-picture" 
            allowfullscreen
            loading="lazy">
    </iframe>
</div>'''
            duration = 15
        else:
            content = f'<div style="text-align: center;"><img src="http://127.0.0.1:8000/api/uploads/images/{lesson["image"]}" alt="{lesson["title"]}" style="max-width: 100%; height: auto;" /></div>'
            duration = 5
        
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": lesson["title"],
            "content_type": "text",
            "content": content,
            "duration_minutes": duration,
            "order": lesson["order"]
        })
        print(f"Added: {lesson['title']}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
