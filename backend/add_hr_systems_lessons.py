import asyncio, os, uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE = "http://localhost:8000/uploads/images/HR/human_resource_systems"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/human_resource_systems{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

lessons_data = [
    {"title": "Human Resource Systems - Slide 1", "type": "text", "content": img(1)},
    {"title": "Human Resource", "type": "embed", "content": vid("https://player.vimeo.com/video/911774773?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Essential Human Resource Systems", "type": "embed", "content": vid("https://player.vimeo.com/video/911774781?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Organization Structure and Reporting Relationships", "type": "embed", "content": vid("https://player.vimeo.com/video/911774791?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Designing Organizational Structure", "type": "embed", "content": vid("https://player.vimeo.com/video/911774797?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Bands and Grades", "type": "embed", "content": vid("https://player.vimeo.com/video/911774805?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Designing Bands and Grades Structure", "type": "embed", "content": vid("https://player.vimeo.com/video/911774814?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Need for Human Resource Policies", "type": "embed", "content": vid("https://player.vimeo.com/video/911774841?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Setting up Your Company's Policy Framework", "type": "embed", "content": vid("https://player.vimeo.com/video/911774853?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Human Resource Systems - Slide 2", "type": "text", "content": img(2)},
    {"title": "Human Resource Systems - Slide 3", "type": "text", "content": img(3)},
    {"title": "Recruitment: Employee Value Preposition", "type": "embed", "content": vid("https://player.vimeo.com/video/911774871?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Recruitment: Role Outcomes", "type": "embed", "content": vid("https://player.vimeo.com/video/911774893?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Recruitment: Framing the Job Description", "type": "embed", "content": vid("https://player.vimeo.com/video/911774915?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Recruitment Channels", "type": "embed", "content": vid("https://player.vimeo.com/video/911774931?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Recruitment Metrics", "type": "embed", "content": vid("https://player.vimeo.com/video/911774944?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Assessment Tool: Role Plays and Presentation", "type": "embed", "content": vid("https://player.vimeo.com/video/911774950?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Assessment Tool: Situational Response and Group Discussions", "type": "embed", "content": vid("https://player.vimeo.com/video/911774957?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Assessment Tool: Interviews", "type": "embed", "content": vid("https://player.vimeo.com/video/911774965?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Assessment Form", "type": "embed", "content": vid("https://player.vimeo.com/video/911774973?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Onboarding and Induction", "type": "embed", "content": vid("https://player.vimeo.com/video/911774986?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Human Resource Systems - Slide 5", "type": "text", "content": img(5)},
    {"title": "Human Resource Systems - Slide 6", "type": "text", "content": img(6)},
    {"title": "Human Resource Systems - Slide 7", "type": "text", "content": img(7)},
    {"title": "Performance Management System", "type": "embed", "content": vid("https://player.vimeo.com/video/911775047?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Goal Setting", "type": "embed", "content": vid("https://player.vimeo.com/video/911774991?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Setting up Key Results Areas for Your Company", "type": "embed", "content": vid("https://player.vimeo.com/video/911774995?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Sharing Key Results Areas with the Team Members", "type": "embed", "content": vid("https://player.vimeo.com/video/911775006?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Conducting Objective and Performance Reviews", "type": "embed", "content": vid("https://player.vimeo.com/video/911775009?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Providing Effective Feedback", "type": "embed", "content": vid("https://player.vimeo.com/video/911775018?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Action Planning", "type": "embed", "content": vid("https://player.vimeo.com/video/911775038?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Human Resource Systems - Slide 8", "type": "text", "content": img(8)},
    {"title": "Human Resource Systems - Slide 9", "type": "text", "content": img(9)},
]

async def main():
    course = await db.courses.find_one({"id": "1691275b-0076-4ee9-add3-11e077ccfa2a"})
    print(f"Course: {course['title']}")
    module = await db.modules.find_one({"course_id": course["id"]})
    await db.lessons.delete_many({"module_id": module["id"]})
    for i, lesson in enumerate(lessons_data):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson["title"],
            "content_type": lesson["type"],
            "content": lesson["content"],
            "duration_minutes": 10,
            "order": i
        })
    print(f"Added {len(lessons_data)} lessons")

asyncio.run(main())
