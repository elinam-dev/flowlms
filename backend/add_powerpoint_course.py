from pymongo import MongoClient
import os
import uuid
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

course = {
    "id": str(uuid.uuid4()),
    "title": "Pumps Spares Presentation",
    "code": "ENG-PUMPS-001",
    "description": "Comprehensive presentation covering pump spare parts, maintenance components, and replacement procedures. Learn about essential spare parts inventory, identification, and proper handling of pump components.",
    "category": "Engineering",
    "type": "optional",
    "duration": "1 hour",
    "thumbnail": "",
    "modules": [
        {
            "title": "Pumps Spares Overview",
            "order": 1,
            "lessons": [
                {
                    "title": "Pumps Spares Presentation",
                    "type": "text",
                    "order": 1,
                    "content": '''<div class="lesson-content">
<div style="position: relative; width: 100%; padding-bottom: 56.25%; height: 0; overflow: hidden; background: #f8fafc; border-radius: 8px;">
    <iframe 
        src="https://docs.google.com/presentation/d/e/2PACX-1vQ6M_kQvMrYalQirQ-mYKfcRTc3EbJKTfhZVucicuSvJeCzCwfyyxWI2_ontj0_aQ/embed?start=false&loop=false&delayms=10000" 
        frameborder="0" 
        width="100%" 
        height="100%" 
        allowfullscreen="true" 
        mozallowfullscreen="true" 
        webkitallowfullscreen="true"
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;">
    </iframe>
</div>
<div style="margin-top: 20px; padding: 15px; background-color: #f0f9ff; border-left: 4px solid #095EB1; border-radius: 4px;">
    <p style="margin: 0; color: #1e293b;"><strong>📌 Navigation Tips:</strong></p>
    <ul style="margin: 10px 0 0 0; color: #475569;">
        <li>Use arrow keys (← →) or click the arrows in the presentation to navigate</li>
        <li>Press F11 for fullscreen mode</li>
        <li>Click the presentation to focus before using keyboard controls</li>
    </ul>
</div>
</div>'''
                }
            ]
        }
    ],
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc)
}

result = db.courses.insert_one(course)
print("Course 'Pumps Spares Presentation' added successfully!")
print(f"Course ID: {result.inserted_id}")
print("Category: Engineering")
print("Type: Optional")
print("\nThe presentation is now available in the LMS!")

client.close()
