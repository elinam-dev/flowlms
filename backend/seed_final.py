"""
Seed 16 courses: Engineering, Health & Safety, Personal Branding, French
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

FINAL_COURSES = [
    # Engineering
    {"title": "Mechanical Engineering and Design Concepts", "description": "Master mechanical engineering principles and design concepts for industrial applications.", "code": "ENG-001", "category": "ENGINEERING"},
    {"title": "Diploma in Laws of Thermodynamics", "description": "Comprehensive study of thermodynamic laws and their applications in engineering systems.", "code": "ENG-002", "category": "ENGINEERING"},
    {"title": "Diploma in Mechatronics", "description": "Integration of mechanical, electrical, and computer engineering for automated systems.", "code": "ENG-003", "category": "ENGINEERING"},
    {"title": "Marine Auxiliary Machinery - Pumps, Fans and Blowers", "description": "Specialized training in marine pumps, fans, and blowers for maritime applications.", "code": "ENG-004", "category": "ENGINEERING"},
    
    # Health & Safety
    {"title": "Fundamentals of Health and Safety in the Workplace", "description": "Essential workplace health and safety principles, regulations, and best practices.", "code": "HS-001", "category": "HEALTH & SAFETY"},
    {"title": "Health and Safety - Personal Protective Equipment", "description": "Proper selection, use, and maintenance of personal protective equipment in the workplace.", "code": "HS-002", "category": "HEALTH & SAFETY"},
    {"title": "Health and Safety Well-being - Mental Health", "description": "Promote mental health awareness and well-being in the workplace environment.", "code": "HS-003", "category": "HEALTH & SAFETY"},
    
    # Personal Branding
    {"title": "Personal Branding for Professionals", "description": "Build and manage your professional brand for career success and recognition.", "code": "PB-001", "category": "PERSONAL DEVELOPMENT"},
    {"title": "Telephone Etiquette for Personal Assistants", "description": "Professional telephone communication skills and etiquette for administrative professionals.", "code": "PB-002", "category": "PERSONAL DEVELOPMENT"},
    {"title": "Diploma in Personal Development Skills", "description": "Comprehensive personal development covering communication, time management, and professional growth.", "code": "PB-003", "category": "PERSONAL DEVELOPMENT"},
    {"title": "Workplace Communication Basics", "description": "Essential communication skills for effective workplace interactions and collaboration.", "code": "PB-004", "category": "PERSONAL DEVELOPMENT"},
    {"title": "Effective B2B Communication", "description": "Master business-to-business communication strategies for professional success.", "code": "PB-005", "category": "PERSONAL DEVELOPMENT"},
    {"title": "Emotional Resilience at Work", "description": "Build emotional resilience to handle workplace stress and challenges effectively.", "code": "PB-006", "category": "PERSONAL DEVELOPMENT"},
    {"title": "Motivation - Power Guide to Motivating Yourself and Others", "description": "Techniques for self-motivation and inspiring others to achieve goals and excellence.", "code": "PB-007", "category": "PERSONAL DEVELOPMENT"},
    
    # French
    {"title": "Diploma in French Language Studies", "description": "Comprehensive French language training covering grammar, vocabulary, and conversation skills.", "code": "LANG-001", "category": "LANGUAGE"}
]

async def seed_final_courses():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Seeding 16 final courses...")
    
    for i, course_data in enumerate(FINAL_COURSES, 1):
        existing = await db.courses.find_one({"code": course_data["code"]})
        if existing:
            print(f"  {i}. {course_data['title']} - Already exists")
            continue
        
        course_id = str(uuid.uuid4())
        await db.courses.insert_one({
            "id": course_id,
            "title": course_data["title"],
            "description": course_data["description"],
            "code": course_data["code"],
            "category": course_data["category"],
            "course_type": "optional",
            "duration_hours": 8,
            "is_published": True,
            "enrolled_users": [],
            "created_at": "2024-01-01T00:00:00"
        })
        
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course_id,
            "title": "Course Content",
            "description": f"Complete content for {course_data['title']}",
            "order": 0
        })
        
        for page_num in range(1, 31):
            lesson_id = str(uuid.uuid4())
            await db.lessons.insert_one({
                "id": lesson_id,
                "module_id": module_id,
                "title": f"Page {page_num}: {get_lesson_title(page_num, course_data['category'])}",
                "content_type": "text",
                "content": generate_lesson_content(page_num, course_data['title'], course_data['category']),
                "duration_minutes": 10,
                "order": page_num - 1
            })
        
        quiz_id = str(uuid.uuid4())
        await db.quizzes.insert_one({
            "id": quiz_id,
            "module_id": module_id,
            "title": f"{course_data['title']} - Final Assessment",
            "description": f"Test your knowledge of {course_data['title']}. You need 70% to pass.",
            "passing_score": 70,
            "questions": generate_quiz_questions(course_data['category']),
            "time_limit_minutes": 24,
            "created_at": "2024-01-01T00:00:00"
        })
        
        print(f"  ✓ {i}. {course_data['title']}")
    
    print("\n✅ All final courses seeded!")
    client.close()

def get_lesson_title(page_num, category):
    titles = {
        "ENGINEERING": ["Introduction", "Fundamentals", "Principles", "Design Concepts", "Materials", "Mechanics", "Thermodynamics", "Fluid Dynamics", "Systems", "Components", "Analysis", "Calculations", "Testing", "Quality", "Standards", "Safety", "Maintenance", "Troubleshooting", "Optimization", "Innovation", "Technology", "Applications", "Case Studies", "Best Practices", "Industry Standards", "Challenges", "Solutions", "Future Trends", "Summary", "Next Steps"],
        "HEALTH & SAFETY": ["Introduction", "Regulations", "Risk Assessment", "Hazard Identification", "Control Measures", "PPE Selection", "Safety Procedures", "Emergency Response", "Incident Reporting", "Investigation", "Prevention", "Training", "Compliance", "Audits", "Documentation", "Communication", "Mental Health", "Well-being", "Stress Management", "Support Systems", "Culture", "Leadership", "Accountability", "Case Studies", "Best Practices", "Common Issues", "Solutions", "Continuous Improvement", "Summary", "Action Plan"],
        "PERSONAL DEVELOPMENT": ["Introduction", "Self-Assessment", "Goal Setting", "Communication Skills", "Active Listening", "Professional Image", "Networking", "Time Management", "Productivity", "Stress Management", "Emotional Intelligence", "Resilience", "Motivation", "Confidence", "Leadership", "Teamwork", "Conflict Resolution", "Problem Solving", "Decision Making", "Adaptability", "Continuous Learning", "Career Development", "Personal Branding", "Digital Presence", "Case Studies", "Best Practices", "Challenges", "Solutions", "Summary", "Action Plan"],
        "LANGUAGE": ["Introduction", "Alphabet & Pronunciation", "Basic Grammar", "Vocabulary Building", "Common Phrases", "Greetings", "Numbers & Time", "Present Tense", "Past Tense", "Future Tense", "Questions", "Negation", "Adjectives", "Adverbs", "Prepositions", "Conversation Practice", "Reading Comprehension", "Writing Skills", "Business French", "Cultural Context", "Idioms", "Advanced Grammar", "Complex Sentences", "Formal vs Informal", "Practice Exercises", "Common Mistakes", "Tips & Tricks", "Resources", "Summary", "Next Steps"]
    }
    category_titles = titles.get(category, titles["PERSONAL DEVELOPMENT"])
    return category_titles[page_num - 1] if page_num <= len(category_titles) else f"Topic {page_num}"

def generate_lesson_content(page_num, course_title, category):
    return f"""<div class="lesson-content">
<h2>{get_lesson_title(page_num, category)}</h2>
<p>Welcome to page {page_num} of <strong>{course_title}</strong>. This lesson provides essential knowledge for Flowitec professionals.</p>

<h3>Learning Objectives</h3>
<div class="highlight-box">
<ul>
<li>Understand key concepts and principles</li>
<li>Apply knowledge in practical situations</li>
<li>Improve professional capabilities</li>
<li>Contribute to organizational success</li>
</ul>
</div>

<h3>Key Concepts</h3>
<p>This content is essential for success at Flowitec, a leading provider of pumps and valves to industries worldwide.</p>

<div class="responsibilities-grid">
<div class="resp-card">
<h4>Knowledge</h4>
<p>Build strong foundational understanding.</p>
<ul><li>Core concepts</li><li>Principles</li><li>Standards</li></ul>
</div>
<div class="resp-card">
<h4>Skills</h4>
<p>Develop practical capabilities.</p>
<ul><li>Application</li><li>Practice</li><li>Mastery</li></ul>
</div>
<div class="resp-card">
<h4>Performance</h4>
<p>Achieve excellence in execution.</p>
<ul><li>Quality</li><li>Efficiency</li><li>Results</li></ul>
</div>
<div class="resp-card">
<h4>Growth</h4>
<p>Continuous improvement and development.</p>
<ul><li>Learning</li><li>Innovation</li><li>Excellence</li></ul>
</div>
</div>

<h3>Practical Application</h3>
<table>
<tr><th>Area</th><th>Application</th><th>Benefit</th></tr>
<tr><td>Daily Work</td><td>Apply concepts in routine tasks</td><td>Improved efficiency and quality</td></tr>
<tr><td>Problem Solving</td><td>Use knowledge to address challenges</td><td>Better solutions and outcomes</td></tr>
<tr><td>Collaboration</td><td>Share expertise with team</td><td>Enhanced team performance</td></tr>
<tr><td>Innovation</td><td>Apply learning to new situations</td><td>Competitive advantage</td></tr>
</table>

<h3>Best Practices</h3>
<div class="info-box">
<h4>Flowitec Standards</h4>
<ul>
<li><strong>Excellence:</strong> Strive for the highest standards</li>
<li><strong>Safety:</strong> Prioritize safety in all activities</li>
<li><strong>Quality:</strong> Deliver quality in every task</li>
<li><strong>Integrity:</strong> Act with honesty and ethics</li>
<li><strong>Teamwork:</strong> Collaborate for success</li>
</ul>
</div>

<h3>Case Study</h3>
<div class="example-box">
<p><strong>Situation:</strong> A Flowitec team applied these principles to improve operations.</p>
<p><strong>Approach:</strong></p>
<ul>
<li>Applied learned concepts systematically</li>
<li>Collaborated across departments</li>
<li>Implemented best practices</li>
<li>Monitored results and adjusted</li>
<li>Shared learnings with organization</li>
</ul>
<p><strong>Result:</strong> Significant improvement in performance and customer satisfaction.</p>
</div>

<div class="highlight-box">
<h4>Key Takeaway</h4>
<p>Apply these principles consistently to contribute to Flowitec's success and your professional growth.</p>
</div>
</div>"""

def generate_quiz_questions(category):
    base_questions = [
        {"question": f"What is the primary focus of this {category.lower()} course?", "question_type": "multiple_choice", "options": ["Ignore principles", "Master key concepts", "Avoid learning", "Skip practice"], "correct_answer": "Master key concepts", "points": 1, "order": 0},
        {"question": "Continuous learning improves professional capabilities.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 1},
        {"question": "What is essential for success?", "question_type": "multiple_choice", "options": ["Avoiding work", "Applying knowledge", "Ignoring standards", "Skipping training"], "correct_answer": "Applying knowledge", "points": 1, "order": 2},
        {"question": "Best practices should be followed consistently.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 3},
        {"question": "What drives improvement?", "question_type": "multiple_choice", "options": ["Avoiding change", "Continuous learning", "Ignoring feedback", "Staying static"], "correct_answer": "Continuous learning", "points": 1, "order": 4},
        {"question": "Safety is a priority in all activities.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 5},
        {"question": "What is key to professional growth?", "question_type": "multiple_choice", "options": ["Avoiding challenges", "Skill development", "Ignoring training", "Staying comfortable"], "correct_answer": "Skill development", "points": 1, "order": 6},
        {"question": "Collaboration enhances team performance.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 7},
        {"question": "What ensures quality?", "question_type": "multiple_choice", "options": ["Rushing work", "Following standards", "Skipping checks", "Ignoring details"], "correct_answer": "Following standards", "points": 1, "order": 8},
        {"question": "Excellence requires consistent effort.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 9},
        {"question": "What is essential for success?", "question_type": "multiple_choice", "options": ["Avoiding responsibility", "Taking initiative", "Ignoring goals", "Waiting passively"], "correct_answer": "Taking initiative", "points": 1, "order": 10},
        {"question": "Professional development is an ongoing process.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 11}
    ]
    return base_questions

if __name__ == "__main__":
    asyncio.run(seed_final_courses())
