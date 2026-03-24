import asyncio, os, uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE = "http://localhost:8000/uploads/images/Finance/basics_of_value-added_tax"

def img(n):
    return f'<div style="text-align: center;"><img src="{BASE}/basics_of_value-added_tax{n}.jpeg" alt="Slide {n}" style="max-width: 100%; height: auto;" /></div>'

def vid(url):
    return f'<iframe src="{url}" width="640" height="360" frameborder="0" allowfullscreen></iframe>'

new_lessons = [
    {"title": "Explaining Tax on Goods and Services", "type": "embed", "content": vid("https://player.vimeo.com/video/753136644?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Procedure of the Reverse Charge System", "type": "embed", "content": vid("https://player.vimeo.com/video/753137138?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Taxing Vehicles", "type": "embed", "content": vid("https://player.vimeo.com/video/753137891?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Defining Value-Added Return", "type": "embed", "content": vid("https://player.vimeo.com/video/753138473?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Paying VAT Bills and Return Refunds", "type": "embed", "content": vid("https://player.vimeo.com/video/753139234?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Understanding VAT Deductions in the UK", "type": "embed", "content": vid("https://player.vimeo.com/video/753140017?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Recommendation on VAT Compliance", "type": "embed", "content": vid("https://player.vimeo.com/video/753140631?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "VAT Health Checks", "type": "embed", "content": vid("https://player.vimeo.com/video/753141416?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Tips for Current and Post Visits Check", "type": "embed", "content": vid("https://player.vimeo.com/video/753144211?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Comprehending VAT Exemptions", "type": "embed", "content": vid("https://player.vimeo.com/video/753145795?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "VAT Sales Exemptions", "type": "embed", "content": vid("https://player.vimeo.com/video/753147601?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Grasping the Zero-Rating Technique", "type": "embed", "content": vid("https://player.vimeo.com/video/753873325?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Justifications for Exemptions and Zero-Rating", "type": "embed", "content": vid("https://player.vimeo.com/video/753874079?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Explaining VAT Fraud and Reverse Charge", "type": "embed", "content": vid("https://player.vimeo.com/video/753885387?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Prohibited Goods, Offences, and Penalties", "type": "embed", "content": vid("https://player.vimeo.com/video/753886796?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Comprehending Tax Evasion Sanctions", "type": "embed", "content": vid("https://player.vimeo.com/video/753888307?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Criminal VAT Prosecution Policy", "type": "embed", "content": vid("https://player.vimeo.com/video/753889412?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Process for Making Taxes Digital (MTD)", "type": "embed", "content": vid("https://player.vimeo.com/video/753891113?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Knowing Softwares Used for Submission", "type": "embed", "content": vid("https://player.vimeo.com/video/753892711?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Updating VAT Records and Preparing for MTD", "type": "embed", "content": vid("https://player.vimeo.com/video/753893335?quality=720p&audiotrack=main&texttrack=en")},
    {"title": "Basics of Value-Added Tax - Slide 9", "type": "text", "content": img(9)},
    {"title": "Basics of Value-Added Tax - Slide 10", "type": "text", "content": img(10)},
    {"title": "Basics of Value-Added Tax - Slide 11", "type": "text", "content": img(11)},
    {"title": "Basics of Value-Added Tax - Slide 12", "type": "text", "content": img(12)},
    {"title": "Basics of Value-Added Tax - Slide 13", "type": "text", "content": img(13)},
    {"title": "Basics of Value-Added Tax - Slide 14", "type": "text", "content": img(14)},
]

async def main():
    course = await db.courses.find_one({"id": "7cc7787d-8050-4432-a5ae-6fc22664fe18"})
    module = await db.modules.find_one({"course_id": course["id"]})
    count = await db.lessons.count_documents({"module_id": module["id"]})

    for i, lesson in enumerate(new_lessons):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module["id"],
            "title": lesson["title"],
            "content_type": lesson["type"],
            "content": lesson["content"],
            "duration_minutes": 10,
            "order": count + i
        })

    print(f"Added {len(new_lessons)} lessons. Total: {count + len(new_lessons)}")

asyncio.run(main())
