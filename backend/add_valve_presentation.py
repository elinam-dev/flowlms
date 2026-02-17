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

# Create course
course_id = str(uuid.uuid4())
course = {
    "id": course_id,
    "title": "Valve Presentation",
    "code": "ENG-VALVE-001",
    "description": "Comprehensive presentation covering valve types, applications, and maintenance procedures. Learn about different valve configurations, selection criteria, and proper installation techniques for industrial applications.",
    "category": "Engineering",
    "type": "optional",
    "duration": "1 hour",
    "thumbnail": "",
    "is_published": True,
    "enrolled_users": [],
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc)
}

db.courses.insert_one(course)
print(f"Created course: {course['title']}")

# Create module
module_id = str(uuid.uuid4())
module = {
    "id": module_id,
    "course_id": course_id,
    "title": "Valve Overview",
    "description": "",
    "order": 1
}
db.modules.insert_one(module)
print(f"Created module: {module['title']}")

# Create lesson with embedded presentation
lesson_id = str(uuid.uuid4())
lesson = {
    "id": lesson_id,
    "module_id": module_id,
    "title": "Valve Presentation",
    "content_type": "text",
    "content": '''<div class="lesson-content">
<div style="position: relative; width: 100%; padding-bottom: 56.25%; height: 0; overflow: hidden; background: #f8fafc; border-radius: 8px;">
    <iframe 
        src="https://docs.google.com/presentation/d/e/2PACX-1vQ6M_kQvMrYalQirQ-mYKfcRTc3EbJKTfhZVucicuSvJeCzCwfyyxWI2_ontj0_aQ/embed?start=false&loop=false&delayms=3000" 
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
    <p style="margin: 0; color: #1e293b;"><strong>Navigation Tips:</strong></p>
    <ul style="margin: 10px 0 0 0; color: #475569;">
        <li>Use arrow keys or click the arrows in the presentation to navigate</li>
        <li>Press F11 for fullscreen mode</li>
        <li>Click the presentation to focus before using keyboard controls</li>
    </ul>
</div>
</div>''',
    "duration_minutes": 10,
    "order": 1
}
db.lessons.insert_one(lesson)
print(f"Created lesson: {lesson['title']}")

print("\nValve Presentation course added successfully!")
print(f"Course ID: {course_id}")

client.close()
