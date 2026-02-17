"""
Seed courses from image folders in uploads/documents
Each folder becomes a course with images as lessons
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

COURSE_MAPPING = {
    "PRESENTATION ON PUMP SPARES": {
        "title": "Presentation on Pump Spares",
        "description": "Comprehensive guide to pump spare parts, identification, maintenance, and replacement procedures for industrial pumps.",
        "code": "ENG-PUMP-001",
        "category": "ENGINEERING",
        "duration_hours": 3
    },
    "PUMP CURVES, SELECTION & MATERIAL CHOOSING": {
        "title": "Pump Curves, Selection & Material Choosing",
        "description": "Learn to read pump curves, select appropriate pumps for applications, and choose the right materials for different operating conditions.",
        "code": "ENG-PUMP-002",
        "category": "ENGINEERING",
        "duration_hours": 4
    },
    "PUMP TYPES, PUMP PARTS & WORKING PRINCIPLES PRESENTATION EDITED": {
        "title": "Pump Types, Parts & Working Principles",
        "description": "Detailed exploration of different pump types, their components, and fundamental working principles in industrial applications.",
        "code": "ENG-PUMP-003",
        "category": "ENGINEERING",
        "duration_hours": 3
    },
    "Valve Presentation": {
        "title": "Industrial Valves - Types and Applications",
        "description": "Complete guide to industrial valves including types, selection criteria, installation, and maintenance procedures.",
        "code": "ENG-VALVE-001",
        "category": "ENGINEERING",
        "duration_hours": 2
    }
}

async def seed_image_courses():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    documents_path = ROOT_DIR / "uploads" / "documents"
    
    print(f"\n{'='*80}")
    print("Seeding Courses from Image Folders")
    print(f"{'='*80}\n")
    
    for folder_name, course_info in COURSE_MAPPING.items():
        folder_path = documents_path / folder_name
        
        if not folder_path.exists():
            print(f"WARNING Folder not found: {folder_name}")
            continue
        
        # Get all PNG images sorted
        images = sorted(folder_path.glob("*.png"))
        
        if not images:
            print(f"WARNING No images found in: {folder_name}")
            continue
        
        print(f"Processing: {course_info['title']}")
        print(f"  Code: {course_info['code']}")
        print(f"  Images: {len(images)}")
        
        # Check if course already exists
        existing = await db.courses.find_one({"code": course_info['code']})
        if existing:
            print(f"  WARNING Course already exists, skipping\n")
            continue
        
        # Create course
        course_id = str(uuid.uuid4())
        await db.courses.insert_one({
            "id": course_id,
            "title": course_info['title'],
            "description": course_info['description'],
            "code": course_info['code'],
            "category": course_info['category'],
            "course_type": "optional",
            "duration_hours": course_info['duration_hours'],
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
            "description": f"Visual presentation for {course_info['title']}",
            "order": 0
        })
        
        # Create lessons from images
        for idx, image_path in enumerate(images, 1):
            lesson_id = str(uuid.uuid4())
            
            # Create relative path for serving
            relative_path = f"/uploads/documents/{folder_name}/{image_path.name}"
            
            # Create HTML content with image
            content = f'''<div class="lesson-content">
<div style="text-align: center; padding: 20px;">
<img src="{relative_path}" alt="Slide {idx}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />
</div>
<div style="text-align: center; margin-top: 20px; color: #64748b;">
<p>Slide {idx} of {len(images)}</p>
</div>
</div>'''
            
            await db.lessons.insert_one({
                "id": lesson_id,
                "module_id": module_id,
                "title": f"Slide {idx}",
                "content_type": "text",
                "content": content,
                "duration_minutes": 5,
                "order": idx - 1
            })
        
        # Create quiz
        quiz_id = str(uuid.uuid4())
        quiz_questions = generate_quiz(course_info['title'], course_info['category'])
        
        await db.quizzes.insert_one({
            "id": quiz_id,
            "module_id": module_id,
            "title": f"{course_info['title']} - Assessment",
            "description": f"Test your understanding of {course_info['title']}. Pass mark: 70%",
            "passing_score": 70,
            "questions": quiz_questions,
            "time_limit_minutes": 20,
            "created_at": "2024-01-01T00:00:00"
        })
        
        print(f"  OK Created with {len(images)} slides and {len(quiz_questions)} quiz questions\n")
    
    print(f"{'='*80}")
    print("SUCCESS All image-based courses seeded successfully!")
    print(f"{'='*80}\n")
    
    client.close()

def generate_quiz(title, category):
    """Generate relevant quiz questions based on course"""
    
    if "PUMP SPARES" in title.upper():
        return [
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
        ]
    
    elif "PUMP CURVES" in title.upper() or "SELECTION" in title.upper():
        return [
            {"question": "What does a pump curve show?", "type": "multiple_choice", "options": ["Head vs Flow relationship", "Speed vs Power", "Pressure vs Temperature", "Cost vs Efficiency"], "correct_answer": "Head vs Flow relationship"},
            {"question": "BEP stands for Best Efficiency Point.", "type": "true_false", "correct_answer": "true"},
            {"question": "What happens to head as flow increases?", "type": "short_answer", "correct_answer": "Head decreases"},
            {"question": "Which material is best for corrosive fluids?", "type": "multiple_choice", "options": ["Stainless steel", "Cast iron", "Bronze", "Plastic"], "correct_answer": "Stainless steel"},
            {"question": "What is specific speed?", "type": "short_answer", "correct_answer": "Dimensionless parameter for pump selection"},
            {"question": "Operating at BEP maximizes pump efficiency.", "type": "true_false", "correct_answer": "true"},
            {"question": "What factor determines pump selection?", "type": "multiple_choice", "options": ["Flow and head requirements", "Color preference", "Brand name", "Price only"], "correct_answer": "Flow and head requirements"},
            {"question": "System curves intersect pump curves at the operating point.", "type": "true_false", "correct_answer": "true"},
            {"question": "What is affinity law used for?", "type": "short_answer", "correct_answer": "Predict pump performance at different speeds"},
            {"question": "Which material resists abrasion best?", "type": "multiple_choice", "options": ["Hardened steel", "Aluminum", "Copper", "Plastic"], "correct_answer": "Hardened steel"}
        ]
    
    elif "PUMP TYPES" in title.upper() or "WORKING PRINCIPLES" in title.upper():
        return [
            {"question": "What are the two main pump categories?", "type": "multiple_choice", "options": ["Centrifugal and Positive Displacement", "Electric and Diesel", "Horizontal and Vertical", "Small and Large"], "correct_answer": "Centrifugal and Positive Displacement"},
            {"question": "Centrifugal pumps use rotating impellers.", "type": "true_false", "correct_answer": "true"},
            {"question": "What principle do centrifugal pumps use?", "type": "short_answer", "correct_answer": "Centrifugal force"},
            {"question": "Which pump type is self-priming?", "type": "multiple_choice", "options": ["Positive displacement", "Centrifugal", "Axial flow", "Mixed flow"], "correct_answer": "Positive displacement"},
            {"question": "What is the function of pump volute?", "type": "short_answer", "correct_answer": "Convert velocity to pressure"},
            {"question": "Multistage pumps have multiple impellers.", "type": "true_false", "correct_answer": "true"},
            {"question": "What type of pump is best for high viscosity?", "type": "multiple_choice", "options": ["Positive displacement", "Centrifugal", "Jet pump", "Submersible"], "correct_answer": "Positive displacement"},
            {"question": "Axial flow pumps produce high head.", "type": "true_false", "correct_answer": "false"},
            {"question": "What is a double suction pump?", "type": "short_answer", "correct_answer": "Pump with inlet on both sides of impeller"},
            {"question": "Which pump component converts kinetic energy to pressure?", "type": "multiple_choice", "options": ["Diffuser or volute", "Impeller", "Shaft", "Bearing"], "correct_answer": "Diffuser or volute"}
        ]
    
    else:  # Valve course
        return [
            {"question": "What is the primary function of a valve?", "type": "multiple_choice", "options": ["Control flow", "Generate pressure", "Filter fluid", "Measure flow"], "correct_answer": "Control flow"},
            {"question": "Gate valves are used for throttling.", "type": "true_false", "correct_answer": "false"},
            {"question": "What valve type is best for on/off service?", "type": "short_answer", "correct_answer": "Gate valve or ball valve"},
            {"question": "Which valve allows flow in one direction only?", "type": "multiple_choice", "options": ["Check valve", "Gate valve", "Globe valve", "Butterfly valve"], "correct_answer": "Check valve"},
            {"question": "What is Cv in valve sizing?", "type": "short_answer", "correct_answer": "Flow coefficient"},
            {"question": "Ball valves provide tight shutoff.", "type": "true_false", "correct_answer": "true"},
            {"question": "Which valve is best for throttling?", "type": "multiple_choice", "options": ["Globe valve", "Gate valve", "Check valve", "Plug valve"], "correct_answer": "Globe valve"},
            {"question": "Butterfly valves are quarter-turn valves.", "type": "true_false", "correct_answer": "true"},
            {"question": "What causes valve cavitation?", "type": "short_answer", "correct_answer": "High pressure drop"},
            {"question": "Which valve material resists corrosion best?", "type": "multiple_choice", "options": ["Stainless steel", "Cast iron", "Carbon steel", "Brass"], "correct_answer": "Stainless steel"}
        ]

if __name__ == "__main__":
    asyncio.run(seed_image_courses())
