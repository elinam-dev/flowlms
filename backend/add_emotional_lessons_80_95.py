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
        {"type": "video", "title": "Developing Resilience In Teams", "video_id": "576740039", "order": 79},
        {"type": "video", "title": "Strengthening Resilience In Others", "video_id": "561433252", "order": 80},
        {"type": "image", "title": "Slide 82", "image": "emotional33.jpeg", "order": 81},
        {"type": "image", "title": "Slide 83", "image": "emotional34.jpeg", "order": 82},
        {"type": "video", "title": "Organisational Resilience", "video_id": "576739880", "order": 83},
        {"type": "video", "title": "Working With VUCA", "video_id": "561433418", "order": 84},
        {"type": "image", "title": "Slide 86", "image": "emotional35.jpeg", "order": 85},
        {"type": "video", "title": "The Capacity To Deal With VUCA", "video_id": "561433570", "order": 86},
        {"type": "image", "title": "Slide 88", "image": "emotional36.jpeg", "order": 87},
        {"type": "video", "title": "Building Resilient Organisations", "video_id": "561433650", "order": 88},
        {"type": "video", "title": "The Paradox of Resilience", "video_id": "561433718", "order": 89},
        {"type": "image", "title": "Slide 91", "image": "emotional37.jpeg", "order": 90},
        {"type": "image", "title": "Slide 92", "image": "emotional38.jpeg", "order": 91},
        {"type": "image", "title": "Slide 93", "image": "emotional39.jpeg", "order": 92},
        {"type": "image", "title": "Slide 94", "image": "emotional40.jpeg", "order": 93},
        {"type": "image", "title": "Slide 95", "image": "emotional41.jpeg", "order": 94}
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
