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
    
    # Image lesson
    image_html = '<div style="text-align: center;"><img src="http://127.0.0.1:8000/api/uploads/images/emotional13.jpeg" alt="Slide 30" style="max-width: 100%; height: auto;" /></div>'
    await db.lessons.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module_id,
        "title": "Slide 30",
        "content_type": "text",
        "content": image_html,
        "duration_minutes": 5,
        "order": 29
    })
    print("Added: Slide 30 (image)")
    
    # Video lessons
    lessons = [
        {"title": "Depression / Despair - \"Who Am I?\"", "video_id": "561395385", "order": 30},
        {"title": "Hostility - \"I'm Going To Make This Work If It Kills Me!\"", "video_id": "561395448", "order": 31},
        {"title": "Acceptance - \"I Can See Myself In The Future.\"", "video_id": "561395544", "order": 32},
        {"title": "Moving Forward - \"This Can Work And Be Good!\"", "video_id": "561395617", "order": 33}
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
