from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# New embed content
new_content = '''<div class="lesson-content">
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
</div>'''

# Find the Pumps Spares course
pumps_course = db.courses.find_one({"code": "ENG-PUMPS-001"})

if pumps_course:
    # Find the module
    module = db.modules.find_one({"course_id": pumps_course['id']})
    
    if module:
        # Update the lesson content
        result = db.lessons.update_one(
            {"module_id": module['id']},
            {"$set": {"content": new_content}}
        )
        
        if result.modified_count > 0:
            print("Successfully updated Pumps Spares Presentation with new embed link!")
        else:
            print("Lesson found but no changes made (content might be the same)")
    else:
        print("Module not found!")
else:
    print("Course not found!")

client.close()
