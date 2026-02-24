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
        {"title": "Resilience in Change", "video_id": "561394746", "order": 21},
        {"title": "The Emotions In Change", "video_id": "561394851", "order": 22},
        {"title": "Personal Transition Through Change", "video_id": "561394915", "order": 23},
        {"title": "Anxiety - \"Can I Cope?\"", "video_id": "561395027", "order": 24},
        {"title": "Happiness - \"At Last Something is Going to Change\"", "video_id": "561395090", "order": 25}
    ]
    
    for lesson in lessons:
        video_html = f'''<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
    <iframe src="https://player.vimeo.com/video/{lesson["video_id"]}?quality=720p&audiotrack=main&texttrack=en" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
            frameborder="0" 
            allow="autoplay; fullscreen; picture-in-picture" 
            allowfullscreen
            loading="lazy">
    </iframe>
</div>'''
        
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": lesson["title"],
            "content_type": "text",
            "content": video_html,
            "duration_minutes": 15,
            "order": lesson["order"]
        })
        print(f"Added: {lesson['title']}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
