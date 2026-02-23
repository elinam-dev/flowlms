import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def fix():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"code": "SOFT-MOT-001"})
    module = await db.modules.find_one({"course_id": course["id"]})
    lesson = await db.lessons.find_one({"module_id": module["id"]})
    
    video_html = '''<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
    <iframe src="https://player.vimeo.com/video/346354555?quality=720p&audiotrack=main&texttrack=en" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
            frameborder="0" 
            allow="autoplay; fullscreen; picture-in-picture" 
            allowfullscreen>
    </iframe>
</div>'''
    
    await db.lessons.update_one(
        {"id": lesson["id"]},
        {"$set": {"content": video_html, "content_type": "text"}}
    )
    
    print("Updated video lesson with iframe embed")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix())
