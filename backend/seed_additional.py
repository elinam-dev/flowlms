"""
Seed 2 additional HR courses and 7 Management courses
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

ADDITIONAL_COURSES = [
    # HR Courses
    {"title": "How to Design Performance Management System", "description": "Learn to design and implement effective performance management systems that drive results and employee development.", "code": "HR-019", "category": "HUMAN RESOURCES"},
    {"title": "Behavioral Interviewing Techniques for Employers", "description": "Master behavioral interviewing methods to assess candidates effectively and make better hiring decisions.", "code": "HR-020", "category": "HUMAN RESOURCES"},
    
    # Management Courses
    {"title": "Employee Management for Business Managers", "description": "Essential employee management skills for business managers including motivation, delegation, and team leadership.", "code": "MGT-001", "category": "MANAGEMENT"},
    {"title": "Leadership and Management for Managers", "description": "Develop leadership capabilities and management skills for effective workforce and work management.", "code": "MGT-002", "category": "MANAGEMENT"},
    {"title": "Diploma in Management for New Managers", "description": "Comprehensive management training for new managers covering planning, organizing, leading, and controlling.", "code": "MGT-003", "category": "MANAGEMENT"},
    {"title": "Effective Communication Skills for Managers", "description": "Master communication techniques essential for managerial success including presentations, meetings, and feedback.", "code": "MGT-004", "category": "MANAGEMENT"},
    {"title": "Line Management Essential Skills and Concepts", "description": "Core line management skills including supervision, performance management, and team development.", "code": "MGT-005", "category": "MANAGEMENT"},
    {"title": "Executive Strategy and Management", "description": "Strategic management for executives covering vision, strategy formulation, and organizational leadership.", "code": "MGT-006", "category": "MANAGEMENT"},
    {"title": "Conflict Management and Resolution", "description": "Techniques for managing and resolving workplace conflicts effectively and professionally.", "code": "MGT-007", "category": "MANAGEMENT"}
]

async def seed_additional_courses():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Seeding 2 HR + 7 Management courses...")
    
    for i, course_data in enumerate(ADDITIONAL_COURSES, 1):
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
    
    print("\n✅ All additional courses seeded!")
    client.close()

def get_lesson_title(page_num, category):
    if category == "MANAGEMENT":
        titles = ["Introduction to Management", "Leadership Fundamentals", "Team Building", "Decision Making", "Strategic Planning", "Delegation Skills", "Motivation Techniques", "Performance Management", "Communication", "Conflict Resolution", "Change Management", "Time Management", "Problem Solving", "Goal Setting", "Coaching & Mentoring", "Accountability", "Feedback Skills", "Meeting Management", "Project Management", "Resource Allocation", "Risk Management", "Innovation", "Organizational Culture", "Ethics in Management", "Case Studies", "Best Practices", "Common Challenges", "Solutions", "Future Trends", "Action Plan"]
    else:
        titles = ["Introduction", "Core Concepts", "Assessment Methods", "Best Practices", "Implementation", "Tools & Techniques", "Legal Considerations", "Communication", "Documentation", "Analysis", "Evaluation", "Improvement", "Technology", "Metrics", "Stakeholders", "Planning", "Execution", "Monitoring", "Reporting", "Compliance", "Quality", "Efficiency", "Innovation", "Case Studies", "Applications", "Challenges", "Solutions", "Trends", "Summary", "Next Steps"]
    return titles[page_num - 1] if page_num <= len(titles) else f"Topic {page_num}"

def generate_lesson_content(page_num, course_title, category):
    context = "management excellence" if category == "MANAGEMENT" else "HR effectiveness"
    return f"""<div class="lesson-content">
<h2>{get_lesson_title(page_num, category)}</h2>
<p>Welcome to page {page_num} of <strong>{course_title}</strong>. This lesson provides essential knowledge for {context} at Flowitec.</p>

<h3>Learning Objectives</h3>
<div class="highlight-box">
<ul>
<li>Understand key concepts and principles</li>
<li>Apply best practices in daily operations</li>
<li>Improve team performance and results</li>
<li>Drive organizational success</li>
</ul>
</div>

<h3>Key Concepts</h3>
<p>{"Effective management" if category == "MANAGEMENT" else "Strong HR practices"} {"drives" if category == "MANAGEMENT" else "support"} Flowitec's success in the pumps and valves industry. {"Leaders" if category == "MANAGEMENT" else "HR professionals"} who master these skills contribute significantly to business results.</p>

<div class="responsibilities-grid">
<div class="resp-card">
<h4>Strategic Thinking</h4>
<p>Align actions with organizational goals and vision.</p>
<ul><li>Goal alignment</li><li>Planning</li><li>Decision making</li></ul>
</div>
<div class="resp-card">
<h4>People Development</h4>
<p>Develop capabilities and potential in team members.</p>
<ul><li>Coaching</li><li>Training</li><li>Mentoring</li></ul>
</div>
<div class="resp-card">
<h4>Performance Excellence</h4>
<p>Drive high performance through clear expectations.</p>
<ul><li>Goal setting</li><li>Feedback</li><li>Recognition</li></ul>
</div>
<div class="resp-card">
<h4>Communication</h4>
<p>Communicate effectively with all stakeholders.</p>
<ul><li>Clarity</li><li>Listening</li><li>Transparency</li></ul>
</div>
</div>

<h3>Practical Application</h3>
<table>
<tr><th>Situation</th><th>Challenge</th><th>Solution</th></tr>
<tr><td>Team Performance</td><td>Low productivity</td><td>Clear goals, feedback, and support</td></tr>
<tr><td>Conflict</td><td>Team disagreements</td><td>Active listening and mediation</td></tr>
<tr><td>Change</td><td>Resistance</td><td>Communication and involvement</td></tr>
<tr><td>Development</td><td>Skill gaps</td><td>Training and coaching programs</td></tr>
</table>

<h3>Best Practices</h3>
<div class="info-box">
<h4>Flowitec Standards</h4>
<ul>
<li><strong>Lead by example:</strong> Model the behavior you expect</li>
<li><strong>Communicate clearly:</strong> Ensure understanding and alignment</li>
<li><strong>Develop people:</strong> Invest in team growth and capability</li>
<li><strong>Drive results:</strong> Focus on outcomes and performance</li>
<li><strong>Act with integrity:</strong> Maintain ethical standards always</li>
</ul>
</div>

<h3>Case Study</h3>
<div class="example-box">
<p><strong>Situation:</strong> A Flowitec team was struggling with low morale and productivity.</p>
<p><strong>Approach:</strong></p>
<ul>
<li>Conducted team assessment and feedback sessions</li>
<li>Clarified goals and expectations</li>
<li>Provided coaching and development support</li>
<li>Recognized achievements and progress</li>
<li>Improved communication and collaboration</li>
</ul>
<p><strong>Result:</strong> 40% improvement in productivity and significantly higher team engagement.</p>
</div>

<div class="highlight-box">
<h4>Key Takeaway</h4>
<p>{"Effective management" if category == "MANAGEMENT" else "Strong HR practices"} {"creates" if category == "MANAGEMENT" else "create"} high-performing teams that drive Flowitec's success.</p>
</div>
</div>"""

def generate_quiz_questions(category):
    if category == "MANAGEMENT":
        return [
            {"question": "What is the primary role of a manager?", "question_type": "multiple_choice", "options": ["Do all the work", "Lead and coordinate team", "Avoid decisions", "Micromanage"], "correct_answer": "Lead and coordinate team", "points": 1, "order": 0},
            {"question": "Effective delegation empowers team members.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 1},
            {"question": "What is a key leadership skill?", "question_type": "multiple_choice", "options": ["Avoiding people", "Effective communication", "Ignoring feedback", "Micromanaging"], "correct_answer": "Effective communication", "points": 1, "order": 2},
            {"question": "Conflict in teams should be addressed promptly.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 3},
            {"question": "What drives team motivation?", "question_type": "multiple_choice", "options": ["Fear", "Recognition and purpose", "Punishment", "Confusion"], "correct_answer": "Recognition and purpose", "points": 1, "order": 4},
            {"question": "Managers should provide regular feedback.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 5},
            {"question": "What is strategic planning?", "question_type": "multiple_choice", "options": ["Daily tasks", "Long-term goal setting", "Avoiding decisions", "Reactive management"], "correct_answer": "Long-term goal setting", "points": 1, "order": 6},
            {"question": "Change management requires clear communication.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 7},
            {"question": "What is coaching?", "question_type": "multiple_choice", "options": ["Telling people what to do", "Guiding development", "Avoiding interaction", "Criticizing only"], "correct_answer": "Guiding development", "points": 1, "order": 8},
            {"question": "Time management improves productivity.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 9},
            {"question": "What is accountability?", "question_type": "multiple_choice", "options": ["Blaming others", "Taking responsibility", "Avoiding tasks", "Delegating everything"], "correct_answer": "Taking responsibility", "points": 1, "order": 10},
            {"question": "Leaders should model desired behaviors.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 11}
        ]
    else:
        return [
            {"question": "What is performance management?", "question_type": "multiple_choice", "options": ["Punishing employees", "Continuous improvement process", "Annual review only", "Avoiding feedback"], "correct_answer": "Continuous improvement process", "points": 1, "order": 0},
            {"question": "Behavioral interviewing focuses on past behavior.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 1},
            {"question": "What is a STAR interview method?", "question_type": "multiple_choice", "options": ["Situation, Task, Action, Result", "Simple, True, Accurate, Real", "Start, Talk, Ask, Review", "None of these"], "correct_answer": "Situation, Task, Action, Result", "points": 1, "order": 2},
            {"question": "Performance systems should align with business goals.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 3},
            {"question": "What is the purpose of behavioral questions?", "question_type": "multiple_choice", "options": ["Confuse candidates", "Predict future performance", "Waste time", "Avoid assessment"], "correct_answer": "Predict future performance", "points": 1, "order": 4},
            {"question": "Regular feedback improves performance.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 5},
            {"question": "What should performance goals be?", "question_type": "multiple_choice", "options": ["Vague", "SMART (Specific, Measurable, Achievable, Relevant, Time-bound)", "Impossible", "Optional"], "correct_answer": "SMART (Specific, Measurable, Achievable, Relevant, Time-bound)", "points": 1, "order": 6},
            {"question": "Structured interviews reduce bias.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 7},
            {"question": "What is continuous feedback?", "question_type": "multiple_choice", "options": ["Annual review", "Ongoing communication", "No feedback", "Criticism only"], "correct_answer": "Ongoing communication", "points": 1, "order": 8},
            {"question": "Performance management drives employee development.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 9},
            {"question": "What makes a good interview question?", "question_type": "multiple_choice", "options": ["Yes/no answer", "Open-ended and behavioral", "Confusing", "Irrelevant"], "correct_answer": "Open-ended and behavioral", "points": 1, "order": 10},
            {"question": "Performance systems should be fair and transparent.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 11}
        ]

if __name__ == "__main__":
    asyncio.run(seed_additional_courses())
