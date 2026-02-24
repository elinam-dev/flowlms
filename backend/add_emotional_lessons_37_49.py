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
        {"type": "video", "title": "Characterising Resilience", "video_id": "576739794", "order": 36},
        {"type": "image", "title": "Slide 38", "image": "emotional15.jpeg", "order": 37},
        {"type": "image", "title": "Slide 39", "image": "emotional16.jpeg", "order": 38},
        {"type": "video", "title": "Anti-Fragility", "video_id": "561398652", "order": 39},
        {"type": "video", "title": "Resilience is a Mindset", "video_id": "561398722", "order": 40},
        {"type": "video", "title": "The Capacity to Adapt", "video_id": "561398807", "order": 41},
        {"type": "video", "title": "Energy Levels and Resilience", "video_id": "561398906", "order": 42},
        {"type": "image", "title": "Slide 44", "image": "emotional17.jpeg", "order": 43},
        {"type": "video", "title": "Increasing Levels of Resilience", "video_id": "561399008", "order": 44},
        {"type": "image", "title": "Slide 46", "image": "emotional18.jpeg", "order": 45},
        {"type": "video", "title": "The Body's Reaction to Adversity", "video_id": "576739621", "order": 46},
        {"type": "image", "title": "Slide 48", "image": "emotional19.jpeg", "order": 47},
        {"type": "video", "title": "The Neuroscience of Resilience", "video_id": "561405529", "order": 48}
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
