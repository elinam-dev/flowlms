"""
Update all 4 image-based engineering courses
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

COURSES = {
    "ENG-PUMP-001": {
        "folder": "PRESENTATION ON PUMP SPARES",
        "count": 29
    },
    "ENG-PUMP-002": {
        "folder": "PUMP CURVES, SELECTION & MATERIAL CHOOSING",
        "count": 38
    },
    "ENG-PUMP-003": {
        "folder": "PUMP TYPES, PUMP PARTS & WORKING PRINCIPLES PRESENTATION EDITED",
        "count": 27
    },
    "ENG-VALVE-001": {
        "folder": "Valve Presentation",
        "count": 18
    }
}

async def update_all_image_courses():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    for code, info in COURSES.items():
        course = await db.courses.find_one({"code": code})
        if not course:
            print(f"Course {code} not found")
            continue
        
        module = await db.modules.find_one({"course_id": course['id']})
        await db.lessons.delete_many({"module_id": module['id']})
        
        folder = info['folder']
        count = info['count']
        
        for i in range(1, count + 1):
            image_num = str(i).zfill(2)
            image_path = f"/api/uploads/documents/{folder}/{folder}_{image_num}.png"
            
            content = f'''<div class="lesson-content">
<div style="text-align: center; padding: 20px;">
<img src="{image_path}" alt="Slide {i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />
</div>
<div style="text-align: center; margin-top: 20px; color: #64748b;">
<p>Slide {i} of {count}</p>
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
        
        print(f"OK {course['title']} - {count} slides")
    
    print("\nAll courses updated!")
    client.close()

asyncio.run(update_all_image_courses())
