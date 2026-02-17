import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

async def create_pump_spares():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Create course
    course_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": course_id,
        "title": "Pump Spares",
        "description": "Comprehensive guide to pump spare parts, identification, maintenance, and replacement procedures.",
        "code": "ENG-PUMP-001",
        "category": "ENGINEERING",
        "course_type": "optional",
        "duration_hours": 3,
        "is_published": True,
        "thumbnail": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=400&h=225&fit=crop",
        "enrolled_users": [],
        "created_at": "2024-01-01T00:00:00"
    })
    
    # Create module
    module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": module_id,
        "course_id": course_id,
        "title": "Course Content",
        "description": "Visual presentation for Pump Spares",
        "order": 0
    })
    
    # Create 29 lessons with images
    folder = "PRESENTATION ON PUMP SPARES"
    for i in range(1, 30):
        image_num = str(i).zfill(2)
        image_path = f"/api/uploads/documents/{folder}/{folder}_{image_num}.png"
        
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
            "module_id": module_id,
            "title": f"Slide {i}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 5,
            "order": i - 1
        })
    
    # Create quiz
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module_id,
        "title": "Pump Spares - Assessment",
        "description": "Test your knowledge of Pump Spares. Pass mark: 70%",
        "passing_score": 70,
        "questions": [
            {"question": "What is the primary function of a pump impeller?", "type": "multiple_choice", "options": ["To create pressure", "To seal the pump", "To support the shaft", "To cool the motor"], "correct_answer": "To create pressure"},
            {"question": "Mechanical seals prevent leakage in centrifugal pumps.", "type": "true_false", "correct_answer": "true"},
            {"question": "What material is commonly used for pump bearings?", "type": "short_answer", "correct_answer": "Steel or bronze"},
            {"question": "Which component protects the pump casing from wear?", "type": "multiple_choice", "options": ["Wear ring", "Shaft sleeve", "Coupling", "Baseplate"], "correct_answer": "Wear ring"},
            {"question": "What is the purpose of a shaft sleeve?", "type": "short_answer", "correct_answer": "Protect shaft from wear and corrosion"},
            {"question": "Pump bearings should be lubricated regularly.", "type": "true_false", "correct_answer": "true"},
            {"question": "What causes cavitation in pumps?", "type": "multiple_choice", "options": ["Low suction pressure", "High discharge pressure", "Excessive speed", "Wrong impeller"], "correct_answer": "Low suction pressure"},
            {"question": "Which spare part requires the most frequent replacement?", "type": "multiple_choice", "options": ["Mechanical seal", "Impeller", "Casing", "Baseplate"], "correct_answer": "Mechanical seal"},
            {"question": "What is NPSH?", "type": "short_answer", "correct_answer": "Net Positive Suction Head"},
            {"question": "Pump alignment affects bearing life.", "type": "true_false", "correct_answer": "true"}
        ],
        "time_limit_minutes": 20,
        "created_at": "2024-01-01T00:00:00"
    })
    
    print("Pump Spares course created with 29 slides!")
    client.close()

asyncio.run(create_pump_spares())
