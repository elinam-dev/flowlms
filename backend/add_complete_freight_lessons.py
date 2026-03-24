#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

LESSONS = [
    {"title": "Introduction", "type": "embed", "content": "https://player.vimeo.com/video/868342065?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Establishing Carrier Qualification Criteria", "type": "embed", "content": "https://player.vimeo.com/video/868344014?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Safety and Compliance Considerations", "type": "embed", "content": "https://player.vimeo.com/video/868337505?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Insurance Requirements for Carriers", "type": "embed", "content": "https://player.vimeo.com/video/868337540?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Contracting and Working with Preferred Carriers", "type": "embed", "content": "https://player.vimeo.com/video/868328132?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "type": "embed", "content": "https://player.vimeo.com/video/868327357?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction", "type": "embed", "content": "https://player.vimeo.com/video/868350865?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Road Transportation", "type": "embed", "content": "https://player.vimeo.com/video/868353258?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Rail Transportation", "type": "embed", "content": "https://player.vimeo.com/video/868353473?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Air Transportation", "type": "embed", "content": "https://player.vimeo.com/video/868353032?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Types of Aircraft", "type": "embed", "content": "https://player.vimeo.com/video/868351968?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Water Transportation", "type": "embed", "content": "https://player.vimeo.com/video/868359350?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Pipeline Transportation", "type": "embed", "content": "https://player.vimeo.com/video/868361578?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Intermodal Transportation and Logistics", "type": "embed", "content": "https://player.vimeo.com/video/868359651?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "type": "embed", "content": "https://player.vimeo.com/video/868358272?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction", "type": "embed", "content": "https://player.vimeo.com/video/868364810?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Developing a Marketing Strategy", "type": "embed", "content": "https://player.vimeo.com/video/868368228?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Online and Digital Marketing Strategies", "type": "embed", "content": "https://player.vimeo.com/video/868367121?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Branding and Positioning", "type": "embed", "content": "https://player.vimeo.com/video/868367410?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "type": "embed", "content": "https://player.vimeo.com/video/868365191?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Introduction", "type": "embed", "content": "https://player.vimeo.com/video/868370911?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Identifying and Managing Risks", "type": "embed", "content": "https://player.vimeo.com/video/868374700?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Problem Solving Techniques", "type": "embed", "content": "https://player.vimeo.com/video/868373963?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Handling Claims and Disputes", "type": "embed", "content": "https://player.vimeo.com/video/868374168?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Crisis Management and Contingency Planning", "type": "embed", "content": "https://player.vimeo.com/video/868374318?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Highlights", "type": "embed", "content": "https://player.vimeo.com/video/868371596?quality=720p&audiotrack=main&texttrack=en"},
    {"title": "Freight Broker Diagram 4", "type": "image", "content": "/uploads/images/freight/freight5.jpeg"}
]

async def add_complete_freight_lessons():
    course = await db.courses.find_one({
        "title": {"$regex": "freight.*broker.*training", "$options": "i"}
    })
    
    module = await db.modules.find_one({"course_id": course["id"]})
    
    start_order = 29
    for i, lesson_data in enumerate(LESSONS):
        if lesson_data["type"] == "embed":
            content = f'<div style="text-align: center;"><iframe src="{lesson_data["content"]}" width="960" height="540" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
        else:
            content = f'<div style="text-align: center; padding: 20px;"><img src="{lesson_data["content"]}" alt="{lesson_data["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        
        lesson_doc = {
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson_data["title"],
            "content_type": "text" if lesson_data["type"] == "image" else "embed",
            "content": content,
            "duration_minutes": 10 if lesson_data["type"] == "embed" else 5,
            "order": start_order + i
        }
        
        await db.lessons.insert_one(lesson_doc)
        print(f"Added: {lesson_data['title']}")
    
    print(f"\nAdded {len(LESSONS)} lessons")

if __name__ == "__main__":
    asyncio.run(add_complete_freight_lessons())
