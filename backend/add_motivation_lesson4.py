import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
    module_id = modules[0]["id"]
    
    video_html = '''<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
    <iframe src="https://player.vimeo.com/video/346354969?quality=720p&audiotrack=main&texttrack=en" 
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
        "title": "Other Factors",
        "content_type": "text",
        "content": video_html,
        "duration_minutes": 15,
        "order": 3
    })
    
    print("Added lesson: Other Factors")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
