"""
Seed 10 Supply Chain courses
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

SUPPLY_CHAIN_COURSES = [
    {
        "title": "Introduction to International Commercial Terms (Incoterms)",
        "description": "Master the fundamentals of Incoterms and their application in international trade. Learn how to use these standardized terms to define responsibilities in global transactions.",
        "code": "SC-001"
    },
    {
        "title": "Diploma in Supply Chain Management",
        "description": "Comprehensive training in supply chain management covering procurement, logistics, inventory management, and strategic planning for efficient operations.",
        "code": "SC-002"
    },
    {
        "title": "Understanding Supply Chain Risk Management",
        "description": "Learn to identify, assess, and mitigate risks in supply chain operations. Develop strategies to ensure business continuity and resilience.",
        "code": "SC-003"
    },
    {
        "title": "B2B Supply Chain Management",
        "description": "Explore business-to-business supply chain dynamics, relationship management, and strategies for optimizing B2B logistics and procurement.",
        "code": "SC-004"
    },
    {
        "title": "Supply Chain Ecosystems & Six Sigma Fundamentals",
        "description": "Understand supply chain ecosystems and learn to apply Six Sigma methodologies to improve quality and efficiency in supply chain processes.",
        "code": "SC-005"
    },
    {
        "title": "International Marketing and Supply Chain Management",
        "description": "Integrate marketing strategies with supply chain operations in global markets. Learn to align supply and demand across international boundaries.",
        "code": "SC-006"
    },
    {
        "title": "Freight Broker Training",
        "description": "Comprehensive training for freight brokers covering regulations, negotiations, carrier relationships, and logistics coordination.",
        "code": "SC-007"
    },
    {
        "title": "The Complete Guide to Sea Export Forwarding",
        "description": "Master sea freight forwarding operations including documentation, customs procedures, shipping terms, and international regulations.",
        "code": "SC-008"
    },
    {
        "title": "Warehouse Management: Principles, Trends and Processes",
        "description": "Learn modern warehouse management techniques, inventory control systems, automation trends, and best practices for efficient operations.",
        "code": "SC-009"
    },
    {
        "title": "Lean Six Sigma: White Belt",
        "description": "Introduction to Lean Six Sigma methodology. Learn basic concepts, tools, and techniques for process improvement and waste reduction.",
        "code": "SC-010"
    }
]

async def seed_supply_chain_courses():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Seeding 10 Supply Chain courses...")
    
    for i, course_data in enumerate(SUPPLY_CHAIN_COURSES, 1):
        # Check if course exists
        existing = await db.courses.find_one({"code": course_data["code"]})
        if existing:
            print(f"  {i}. {course_data['title']} - Already exists")
            continue
        
        # Create course
        course_id = str(uuid.uuid4())
        await db.courses.insert_one({
            "id": course_id,
            "title": course_data["title"],
            "description": course_data["description"],
            "code": course_data["code"],
            "category": "SUPPLY CHAIN",
            "course_type": "optional",
            "duration_hours": 8,
            "is_published": True,
            "enrolled_users": [],
            "created_at": "2024-01-01T00:00:00"
        })
        
        # Create module
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course_id,
            "title": "Course Content",
            "description": f"Complete content for {course_data['title']}",
            "order": 0
        })
        
        # Create 30 lessons
        for page_num in range(1, 31):
            lesson_id = str(uuid.uuid4())
            await db.lessons.insert_one({
                "id": lesson_id,
                "module_id": module_id,
                "title": f"Page {page_num}: {get_lesson_title(page_num, course_data['title'])}",
                "content_type": "text",
                "content": generate_lesson_content(page_num, course_data['title']),
                "duration_minutes": 10,
                "order": page_num - 1
            })
        
        # Create quiz
        quiz_id = str(uuid.uuid4())
        questions = generate_quiz_questions(course_data['title'])
        await db.quizzes.insert_one({
            "id": quiz_id,
            "module_id": module_id,
            "title": f"{course_data['title']} - Final Assessment",
            "description": f"Test your knowledge of {course_data['title']}. You need 70% to pass.",
            "passing_score": 70,
            "questions": questions,
            "time_limit_minutes": len(questions) * 2,
            "created_at": "2024-01-01T00:00:00"
        })
        
        print(f"  ✓ {i}. {course_data['title']} - Created with 30 pages and quiz")
    
    print("\n✅ All Supply Chain courses seeded!")
    client.close()

def get_lesson_title(page_num, course_title):
    titles = [
        "Introduction and Overview",
        "Key Concepts and Terminology",
        "Historical Context and Evolution",
        "Industry Standards and Best Practices",
        "Regulatory Framework",
        "Strategic Planning Fundamentals",
        "Operational Excellence",
        "Process Optimization",
        "Technology and Innovation",
        "Data Analysis and Metrics",
        "Risk Assessment",
        "Quality Management",
        "Cost Control Strategies",
        "Performance Measurement",
        "Stakeholder Management",
        "Communication Strategies",
        "Problem-Solving Techniques",
        "Decision-Making Frameworks",
        "Implementation Planning",
        "Change Management",
        "Team Collaboration",
        "Leadership Principles",
        "Continuous Improvement",
        "Case Studies and Examples",
        "Real-World Applications",
        "Common Challenges",
        "Solutions and Workarounds",
        "Future Trends",
        "Summary and Key Takeaways",
        "Next Steps and Resources"
    ]
    return titles[page_num - 1] if page_num <= len(titles) else f"Advanced Topic {page_num}"

def generate_lesson_content(page_num, course_title):
    return f"""<div class="lesson-content">
<h2>{get_lesson_title(page_num, course_title)}</h2>
<p>Welcome to page {page_num} of <strong>{course_title}</strong>. This lesson provides essential knowledge for supply chain professionals at Flowitec.</p>

<h3>Learning Objectives</h3>
<div class="highlight-box">
<p>By the end of this lesson, you will be able to:</p>
<ul>
<li>Understand key concepts related to {get_lesson_title(page_num, course_title).lower()}</li>
<li>Apply these principles in supply chain operations</li>
<li>Improve efficiency in Flowitec's logistics and procurement</li>
<li>Contribute to operational excellence</li>
</ul>
</div>

<h3>Key Concepts</h3>
<p>Supply chain management is critical for Flowitec's success in delivering pumps and valves to customers worldwide. Effective supply chain operations ensure timely delivery, cost efficiency, and customer satisfaction.</p>

<div class="responsibilities-grid">
<div class="resp-card">
<h4>Planning & Strategy</h4>
<p>Strategic planning ensures alignment between supply chain operations and business objectives.</p>
<ul>
<li>Demand forecasting</li>
<li>Capacity planning</li>
<li>Resource allocation</li>
</ul>
</div>

<div class="resp-card">
<h4>Execution & Operations</h4>
<p>Efficient execution of supply chain processes drives operational excellence.</p>
<ul>
<li>Order processing</li>
<li>Inventory management</li>
<li>Logistics coordination</li>
</ul>
</div>

<div class="resp-card">
<h4>Monitoring & Control</h4>
<p>Continuous monitoring ensures supply chain performance meets targets.</p>
<ul>
<li>KPI tracking</li>
<li>Quality control</li>
<li>Performance analysis</li>
</ul>
</div>

<div class="resp-card">
<h4>Improvement & Innovation</h4>
<p>Ongoing improvement drives competitive advantage in supply chain operations.</p>
<ul>
<li>Process optimization</li>
<li>Technology adoption</li>
<li>Best practice implementation</li>
</ul>
</div>
</div>

<h3>Practical Application</h3>
<p>At Flowitec, supply chain excellence is essential for delivering pumps and valves to customers across industries:</p>

<table>
<tr><th>Application</th><th>Challenge</th><th>Solution</th></tr>
<tr><td>Procurement</td><td>Supplier reliability</td><td>Vendor management and diversification</td></tr>
<tr><td>Inventory</td><td>Stock optimization</td><td>Just-in-time and safety stock strategies</td></tr>
<tr><td>Logistics</td><td>Delivery efficiency</td><td>Route optimization and carrier partnerships</td></tr>
<tr><td>Warehousing</td><td>Space utilization</td><td>Layout optimization and automation</td></tr>
</table>

<h3>Best Practices</h3>
<div class="info-box">
<h4>Flowitec Supply Chain Standards</h4>
<ul>
<li><strong>Plan ahead:</strong> Forecast demand and plan resources accordingly</li>
<li><strong>Communicate clearly:</strong> Maintain transparency with suppliers and customers</li>
<li><strong>Monitor performance:</strong> Track KPIs and address issues promptly</li>
<li><strong>Optimize continuously:</strong> Seek improvements in all processes</li>
<li><strong>Manage risks:</strong> Identify and mitigate supply chain vulnerabilities</li>
</ul>
</div>

<h3>Case Study</h3>
<div class="example-box">
<p><strong>Situation:</strong> A mining customer needed urgent delivery of replacement pumps to avoid production downtime.</p>
<p><strong>Flowitec Approach:</strong></p>
<ul>
<li>Expedited order processing and production scheduling</li>
<li>Coordinated with logistics partners for express shipping</li>
<li>Maintained communication with customer throughout</li>
<li>Delivered pumps within 48 hours</li>
<li>Prevented costly production delays for customer</li>
</ul>
<p><strong>Result:</strong> Customer satisfaction increased, leading to expanded partnership and repeat business.</p>
</div>

<h3>Action Items</h3>
<p>To apply what you've learned:</p>
<ul>
<li>Review current supply chain processes in your area</li>
<li>Identify opportunities for improvement</li>
<li>Implement best practices discussed in this lesson</li>
<li>Share insights with your team</li>
<li>Continue to the next lesson to build on this foundation</li>
</ul>

<div class="highlight-box">
<h4>Key Takeaway</h4>
<p>Effective supply chain management is essential for Flowitec's success. By applying these principles, you contribute to operational excellence and customer satisfaction.</p>
</div>
</div>"""

def generate_quiz_questions(course_title):
    questions = [
        {
            "question": "What is the primary goal of supply chain management?",
            "question_type": "multiple_choice",
            "options": ["Reduce costs only", "Optimize flow of goods and services", "Increase inventory", "Eliminate suppliers"],
            "correct_answer": "Optimize flow of goods and services",
            "points": 1,
            "order": 0
        },
        {
            "question": "Which is a key component of supply chain risk management?",
            "question_type": "multiple_choice",
            "options": ["Ignoring risks", "Risk identification and mitigation", "Accepting all risks", "Avoiding suppliers"],
            "correct_answer": "Risk identification and mitigation",
            "points": 1,
            "order": 1
        },
        {
            "question": "What does JIT stand for in supply chain?",
            "question_type": "multiple_choice",
            "options": ["Just In Time", "Join In Trade", "Jump In Transport", "Joint Inventory Tracking"],
            "correct_answer": "Just In Time",
            "points": 1,
            "order": 2
        },
        {
            "question": "Effective communication with suppliers is important.",
            "question_type": "true_false",
            "options": ["True", "False"],
            "correct_answer": "True",
            "points": 1,
            "order": 3
        },
        {
            "question": "What is the purpose of inventory management?",
            "question_type": "multiple_choice",
            "options": ["Maximize stock levels", "Balance supply and demand", "Eliminate all inventory", "Increase storage costs"],
            "correct_answer": "Balance supply and demand",
            "points": 1,
            "order": 4
        },
        {
            "question": "Which metric measures supply chain efficiency?",
            "question_type": "multiple_choice",
            "options": ["Employee satisfaction", "On-time delivery rate", "Office size", "Number of meetings"],
            "correct_answer": "On-time delivery rate",
            "points": 1,
            "order": 5
        },
        {
            "question": "Continuous improvement is essential in supply chain.",
            "question_type": "true_false",
            "options": ["True", "False"],
            "correct_answer": "True",
            "points": 1,
            "order": 6
        },
        {
            "question": "What is a key benefit of supply chain visibility?",
            "question_type": "multiple_choice",
            "options": ["Higher costs", "Better decision making", "More complexity", "Slower processes"],
            "correct_answer": "Better decision making",
            "points": 1,
            "order": 7
        },
        {
            "question": "Supplier relationships should be managed strategically.",
            "question_type": "true_false",
            "options": ["True", "False"],
            "correct_answer": "True",
            "points": 1,
            "order": 8
        },
        {
            "question": "What is the goal of warehouse optimization?",
            "question_type": "multiple_choice",
            "options": ["Maximize space usage", "Efficient storage and retrieval", "Increase handling time", "Reduce automation"],
            "correct_answer": "Efficient storage and retrieval",
            "points": 1,
            "order": 9
        }
    ]
    return questions

if __name__ == "__main__":
    asyncio.run(seed_supply_chain_courses())
