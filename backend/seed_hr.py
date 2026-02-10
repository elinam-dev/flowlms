"""
Seed 18 HR courses
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

HR_COURSES = [
    {"title": "Introduction to Modern Human Resource Management", "description": "Comprehensive introduction to contemporary HR practices, strategies, and the evolving role of HR in organizations.", "code": "HR-001"},
    {"title": "Human Resource Systems and Processes", "description": "Learn HR systems, workflows, and processes for effective people management and organizational efficiency.", "code": "HR-002"},
    {"title": "Diploma in Introduction to Human Resource Concepts", "description": "Foundational HR concepts including recruitment, training, performance management, and employee relations.", "code": "HR-003"},
    {"title": "HR Analytics - Harnessing HR Data for Organization Success", "description": "Use data analytics to drive HR decisions, measure performance, and improve organizational outcomes.", "code": "HR-004"},
    {"title": "Modern Human Resource Management - Recruitment and Selection Process", "description": "Master recruitment strategies, candidate assessment, selection techniques, and hiring best practices.", "code": "HR-005"},
    {"title": "Human Resource Policies and Organization Structure", "description": "Develop effective HR policies and understand organizational structures for optimal workforce management.", "code": "HR-006"},
    {"title": "Onboarding Principles for Employees", "description": "Create effective onboarding programs to integrate new employees and accelerate their productivity.", "code": "HR-007"},
    {"title": "Human Resources: Employee Management and Training", "description": "Effective employee management techniques and training program development for workforce development.", "code": "HR-008"},
    {"title": "Diploma in Strategic HR", "description": "Strategic HR management aligning people strategies with business objectives for competitive advantage.", "code": "HR-009"},
    {"title": "HR: Talent Management and Workforce Development", "description": "Identify, develop, and retain talent while building a skilled and engaged workforce.", "code": "HR-010"},
    {"title": "HRM - The Ultimate Employee Onboarding Guide with 4Cs", "description": "Master the 4Cs of onboarding: Compliance, Clarification, Culture, and Connection for successful integration.", "code": "HR-011"},
    {"title": "Respect Foundations: Diversity, Respect, and Substance Abuse in Workplace", "description": "Foster inclusive workplaces, promote respect, and address substance abuse issues professionally.", "code": "HR-012"},
    {"title": "Human Resources: Discipline and Termination", "description": "Handle disciplinary actions and terminations professionally, legally, and ethically.", "code": "HR-013"},
    {"title": "Competency Mapping in HR: Transform People into Human Capital", "description": "Map competencies, identify skill gaps, and develop employees into valuable human capital.", "code": "HR-014"},
    {"title": "Mastering HR Budget: Strategic Financial Planning for Professionals", "description": "Strategic HR budgeting, cost management, and financial planning for HR initiatives.", "code": "HR-015"},
    {"title": "Employee Onboarding and Motivation", "description": "Combine effective onboarding with motivation strategies to engage and retain employees.", "code": "HR-016"},
    {"title": "Facility Management: Maintenance and Repairs", "description": "Manage workplace facilities, maintenance schedules, and repair operations effectively.", "code": "HR-017"},
    {"title": "Diploma in Strategic Performance Management", "description": "Implement performance management systems that drive results and employee development.", "code": "HR-018"}
]

async def seed_hr_courses():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Seeding 18 HR courses...")
    
    for i, course_data in enumerate(HR_COURSES, 1):
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
            "category": "HUMAN RESOURCES",
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
                "title": f"Page {page_num}: {get_lesson_title(page_num)}",
                "content_type": "text",
                "content": generate_lesson_content(page_num, course_data['title']),
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
            "questions": generate_quiz_questions(),
            "time_limit_minutes": 24,
            "created_at": "2024-01-01T00:00:00"
        })
        
        print(f"  ✓ {i}. {course_data['title']}")
    
    print("\n✅ All HR courses seeded!")
    client.close()

def get_lesson_title(page_num):
    titles = ["Introduction", "Core Concepts", "HR Strategy", "Legal Framework", "Best Practices", "Planning", "Implementation", "Employee Relations", "Performance", "Development", "Compensation", "Benefits", "Compliance", "Technology", "Analytics", "Communication", "Conflict Resolution", "Team Building", "Leadership", "Change Management", "Diversity & Inclusion", "Talent Acquisition", "Retention", "Case Studies", "Real-World Applications", "Common Challenges", "Solutions", "Future Trends", "Summary", "Action Plan"]
    return titles[page_num - 1] if page_num <= len(titles) else f"Topic {page_num}"

def generate_lesson_content(page_num, course_title):
    return f"""<div class="lesson-content">
<h2>{get_lesson_title(page_num)}</h2>
<p>Welcome to page {page_num} of <strong>{course_title}</strong>. This lesson provides essential HR knowledge for Flowitec professionals.</p>

<h3>Learning Objectives</h3>
<div class="highlight-box">
<ul>
<li>Understand key HR concepts and practices</li>
<li>Apply HR strategies in daily operations</li>
<li>Improve employee engagement at Flowitec</li>
<li>Ensure compliance with employment regulations</li>
</ul>
</div>

<h3>Key Concepts</h3>
<p>Human Resource management is vital for Flowitec's success. Effective HR practices attract, develop, and retain talented employees who drive business results.</p>

<div class="responsibilities-grid">
<div class="resp-card">
<h4>Talent Acquisition</h4>
<p>Attract and hire the best talent for Flowitec's needs.</p>
<ul><li>Recruitment strategies</li><li>Candidate assessment</li><li>Selection process</li></ul>
</div>
<div class="resp-card">
<h4>Employee Development</h4>
<p>Develop skills and capabilities for current and future roles.</p>
<ul><li>Training programs</li><li>Career development</li><li>Succession planning</li></ul>
</div>
<div class="resp-card">
<h4>Performance Management</h4>
<p>Drive performance through clear goals and feedback.</p>
<ul><li>Goal setting</li><li>Performance reviews</li><li>Recognition programs</li></ul>
</div>
<div class="resp-card">
<h4>Employee Relations</h4>
<p>Foster positive workplace relationships and culture.</p>
<ul><li>Communication</li><li>Conflict resolution</li><li>Employee engagement</li></ul>
</div>
</div>

<h3>Practical Application</h3>
<table>
<tr><th>HR Function</th><th>Challenge</th><th>Solution</th></tr>
<tr><td>Recruitment</td><td>Finding skilled talent</td><td>Targeted sourcing and employer branding</td></tr>
<tr><td>Retention</td><td>Employee turnover</td><td>Competitive compensation and development opportunities</td></tr>
<tr><td>Training</td><td>Skill gaps</td><td>Comprehensive training programs and mentoring</td></tr>
<tr><td>Engagement</td><td>Low morale</td><td>Recognition programs and open communication</td></tr>
</table>

<h3>Best Practices</h3>
<div class="info-box">
<h4>Flowitec HR Standards</h4>
<ul>
<li><strong>Fair treatment:</strong> Treat all employees with respect and equity</li>
<li><strong>Clear communication:</strong> Maintain transparent and open dialogue</li>
<li><strong>Development focus:</strong> Invest in employee growth and learning</li>
<li><strong>Performance driven:</strong> Set clear expectations and provide feedback</li>
<li><strong>Compliance:</strong> Follow all employment laws and regulations</li>
</ul>
</div>

<h3>Case Study</h3>
<div class="example-box">
<p><strong>Situation:</strong> Flowitec needed to improve employee retention in technical roles.</p>
<p><strong>HR Approach:</strong></p>
<ul>
<li>Conducted employee satisfaction surveys</li>
<li>Implemented career development programs</li>
<li>Enhanced compensation and benefits package</li>
<li>Created mentorship opportunities</li>
<li>Improved work-life balance initiatives</li>
</ul>
<p><strong>Result:</strong> 30% reduction in turnover and increased employee engagement scores.</p>
</div>

<div class="highlight-box">
<h4>Key Takeaway</h4>
<p>Effective HR management creates a positive workplace culture where employees thrive and contribute to Flowitec's success.</p>
</div>
</div>"""

def generate_quiz_questions():
    return [
        {"question": "What is the primary goal of HR management?", "question_type": "multiple_choice", "options": ["Reduce costs", "Manage people effectively", "Increase paperwork", "Avoid employees"], "correct_answer": "Manage people effectively", "points": 1, "order": 0},
        {"question": "Onboarding helps new employees integrate successfully.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 1},
        {"question": "What is the purpose of performance reviews?", "question_type": "multiple_choice", "options": ["Punish employees", "Provide feedback and development", "Reduce salaries", "Create paperwork"], "correct_answer": "Provide feedback and development", "points": 1, "order": 2},
        {"question": "Which is a key component of talent management?", "question_type": "multiple_choice", "options": ["Ignoring employees", "Succession planning", "Avoiding training", "Reducing benefits"], "correct_answer": "Succession planning", "points": 1, "order": 3},
        {"question": "Employee engagement improves productivity.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 4},
        {"question": "What does HR analytics help with?", "question_type": "multiple_choice", "options": ["Data-driven decisions", "Avoiding metrics", "Ignoring trends", "Reducing information"], "correct_answer": "Data-driven decisions", "points": 1, "order": 5},
        {"question": "Diversity and inclusion strengthen organizations.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 6},
        {"question": "What is the 4Cs onboarding model?", "question_type": "multiple_choice", "options": ["Compliance, Clarification, Culture, Connection", "Cost, Control, Change, Communication", "Career, Compensation, Conflict, Compliance", "None of these"], "correct_answer": "Compliance, Clarification, Culture, Connection", "points": 1, "order": 7},
        {"question": "Training and development are essential for employee growth.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 8},
        {"question": "What is the purpose of HR policies?", "question_type": "multiple_choice", "options": ["Create confusion", "Guide behavior and decisions", "Increase complexity", "Avoid clarity"], "correct_answer": "Guide behavior and decisions", "points": 1, "order": 9},
        {"question": "Employee retention is more cost-effective than constant hiring.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 10},
        {"question": "What is strategic HR?", "question_type": "multiple_choice", "options": ["Reactive HR", "Aligning HR with business strategy", "Avoiding planning", "Reducing HR role"], "correct_answer": "Aligning HR with business strategy", "points": 1, "order": 11}
    ]

if __name__ == "__main__":
    asyncio.run(seed_hr_courses())
