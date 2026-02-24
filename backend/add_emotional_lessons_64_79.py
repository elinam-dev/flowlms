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
        {"type": "video", "title": "Action Strategy 1 - Feel in Control", "video_id": "576739772", "order": 63},
        {"type": "image", "title": "Slide 65", "image": "emotional25.jpeg", "order": 64},
        {"type": "video", "title": "Action Strategy 2 - Create a Personal Vision", "video_id": "561424655", "order": 65},
        {"type": "image", "title": "Slide 67", "image": "emotional26.jpeg", "order": 66},
        {"type": "video", "title": "Action Strategy 3 - Be Flexible and Adaptable", "video_id": "561424733", "order": 67},
        {"type": "image", "title": "Slide 69", "image": "emotional27.jpeg", "order": 68},
        {"type": "video", "title": "Action Strategy 4 - Get Organised", "video_id": "561424833", "order": 69},
        {"type": "image", "title": "Slide 71", "image": "emotional28.jpeg", "order": 70},
        {"type": "video", "title": "Action Strategy 5 - A Mindset For Problem Solving", "video_id": "561424914", "order": 71},
        {"type": "image", "title": "Slide 73", "image": "emotional29.jpeg", "order": 72},
        {"type": "video", "title": "Action Strategy 6 - Get Connected", "video_id": "561424985", "order": 73},
        {"type": "image", "title": "Slide 75", "image": "emotional30.jpeg", "order": 74},
        {"type": "video", "title": "Action Strategy 7 - Be Socially Competent", "video_id": "561425051", "order": 75},
        {"type": "image", "title": "Slide 77", "image": "emotional31.jpeg", "order": 76},
        {"type": "video", "title": "Action Strategy 8 - Be Proactive", "video_id": "561425127", "order": 77},
        {"type": "image", "title": "Slide 79", "image": "emotional32.jpeg", "order": 78}
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
