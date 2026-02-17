"""
Update Pump Types course with images
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

async def update_pump_types():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    course = await db.courses.find_one({"code": "ENG-PUMP-003"})
    if not course:
        print("Course not found")
        return
    
    module = await db.modules.find_one({"course_id": course['id']})
    await db.lessons.delete_many({"module_id": module['id']})
    
    folder = "PUMP TYPES, PUMP PARTS & WORKING PRINCIPLES PRESENTATION EDITED"
    
    for i in range(1, 28):
        image_num = str(i).zfill(2)
        image_path = f"/api/uploads/documents/{folder}/{folder}_{image_num}.png"
        
        content = f'''<div class="lesson-content">
<div style="text-align: center; padding: 20px;">
<img src="{image_path}" alt="Slide {i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />
</div>
<div style="text-align: center; margin-top: 20px; color: #64748b;">
<p>Slide {i} of 27</p>
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
    
    print("OK Pump Types course updated with 27 slides")
    client.close()

asyncio.run(update_pump_types())
