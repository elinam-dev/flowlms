import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

async def update_pump_spares():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    course = await db.courses.find_one({"code": "ENG-PUMP-001"})
    module = await db.modules.find_one({"course_id": course['id']})
    
    # Delete old lessons
    await db.lessons.delete_many({"module_id": module['id']})
    
    # Create 29 lessons with correct image paths
    for i in range(1, 30):
        image_num = str(i).zfill(2)
        image_path = f"/api/uploads/images/presentation_on_pump_spares_{image_num}.png"
        
        content = f'''<div class="lesson-content">
<div style="text-align: center; padding: 20px;">
<img src="{image_path}" alt="Slide {i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />
</div>
<div style="text-align: center; margin-top: 20px; color: #64748b;">
<p>Slide {i} of 29</p>
</div>
</div>'''
        
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module['id'],
            "title": f"Slide {i}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 5,
            "order": i - 1
        })
    
    print("Pump Spares updated with images from /api/uploads/images/")
    client.close()

asyncio.run(update_pump_spares())
