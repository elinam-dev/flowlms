import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

async def update_incoterms_with_slides():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Find Incoterms course
    incoterms_course = await db.courses.find_one({"title": {"$regex": "incoterms", "$options": "i"}})
    
    if not incoterms_course:
        print("No Incoterms course found")
        return
    
    # Get lessons
    modules = await db.modules.find({"course_id": incoterms_course["id"]}).to_list(100)
    if not modules:
        print("No modules found")
        return
    
    lessons = await db.lessons.find({"module_id": modules[0]["id"]}).sort("order", 1).to_list(100)
    
    # Map slides to lessons (distribute 86 slides across 12 lessons)
    slide_mapping = {
        0: list(range(1, 8)),      # Overview: slides 1-7
        1: list(range(8, 15)),     # What Are Incoterms: slides 8-14
        2: list(range(15, 22)),    # Why Incoterms Matter: slides 15-21
        3: list(range(22, 29)),    # EXW & FCA: slides 22-28
        4: list(range(29, 36)),    # Sea Freight FAS & FOB: slides 29-35
        5: list(range(36, 43)),    # CFR & CIF: slides 36-42
        6: list(range(43, 50)),    # CPT, CIP & Delivery: slides 43-49
        7: list(range(50, 57)),    # Sea Freight Documentation: slides 50-56
        8: list(range(57, 64)),    # Sea Freight Charges & Ghana: slides 57-63
        9: list(range(64, 71)),    # Nigeria & Kenya: slides 64-70
        10: list(range(71, 78)),   # Risk Management: slides 71-77
        11: list(range(78, 87))    # Final Assessment: slides 78-86
    }
    
    for i, lesson in enumerate(lessons):
        if i in slide_mapping:
            slides = slide_mapping[i]
            
            # Create HTML content with slides
            slide_html = '<div class="incoterms-slides">'
            for slide_num in slides:
                slide_html += f'<div class="slide-container"><img src="/api/uploads/images/incoterms/incoterms{slide_num}.jpeg" alt="Slide {slide_num}" class="slide-image" /></div>'
            slide_html += '</div>'
            
            # Update lesson content
            await db.lessons.update_one(
                {"id": lesson["id"]},
                {"$set": {"content": slide_html, "content_type": "text"}}
            )
            
            print(f"Updated lesson {i+1}: {lesson['title']} with slides {slides[0]}-{slides[-1]}")
    
    print("Successfully updated all Incoterms lessons with slides!")
    client.close()

if __name__ == "__main__":
    asyncio.run(update_incoterms_with_slides())