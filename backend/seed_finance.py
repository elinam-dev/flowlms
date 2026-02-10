"""
Seed 19 Finance courses
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

FINANCE_COURSES = [
    {"title": "Fundamentals of Accounting", "description": "Master the basic principles of accounting including the accounting equation, financial statements, and recording transactions.", "code": "FIN-001"},
    {"title": "Diploma in Financial Accounting", "description": "Comprehensive training in financial accounting covering advanced concepts, reporting standards, and financial statement preparation.", "code": "FIN-002"},
    {"title": "Introduction to Business Accounting", "description": "Learn essential business accounting concepts including bookkeeping, financial records, and basic accounting principles.", "code": "FIN-003"},
    {"title": "Essentials of Throughput Accounting and Lean Accounting", "description": "Explore throughput accounting and lean accounting methodologies for optimizing business performance and reducing waste.", "code": "FIN-004"},
    {"title": "Diploma in Cost Accounting", "description": "Advanced cost accounting techniques including cost allocation, variance analysis, and cost management strategies.", "code": "FIN-005"},
    {"title": "Sage One - Bookkeeping and Accounting", "description": "Practical training in using Sage One software for bookkeeping, invoicing, and financial management.", "code": "FIN-006"},
    {"title": "The Accounting Cycle and Financial Statements", "description": "Understand the complete accounting cycle from journal entries to financial statement preparation and closing.", "code": "FIN-007"},
    {"title": "Master the Double-Entry Accounting System", "description": "Deep dive into double-entry bookkeeping principles, debits and credits, and maintaining balanced accounts.", "code": "FIN-008"},
    {"title": "Tax Accounting Systems and Administration", "description": "Learn tax accounting principles, compliance requirements, and tax administration procedures.", "code": "FIN-009"},
    {"title": "Financial Statement Analysis: Accounting Ratios and Analytical Strategy", "description": "Analyze financial statements using ratios, trends, and strategic analytical frameworks for decision-making.", "code": "FIN-010"},
    {"title": "Cost and Management Accounting: Planning for Effective Strategy Execution", "description": "Strategic cost and management accounting for planning, budgeting, and executing business strategies.", "code": "FIN-011"},
    {"title": "Diploma in Decision Making Using Financial Accounting", "description": "Use financial accounting information for strategic business decisions and performance evaluation.", "code": "FIN-012"},
    {"title": "Accounts Receivable Management", "description": "Effective management of accounts receivable including credit policies, collections, and cash flow optimization.", "code": "FIN-013"},
    {"title": "Accounts Payable Management", "description": "Best practices for managing accounts payable, vendor relationships, and payment processing.", "code": "FIN-014"},
    {"title": "Fundamentals of Budgeting and Variance Analysis", "description": "Learn budgeting techniques, variance analysis, and performance monitoring for financial control.", "code": "FIN-015"},
    {"title": "Essentials of SAP CO - Managing and Controlling Cost", "description": "Master SAP Controlling module for cost management, profitability analysis, and internal reporting.", "code": "FIN-016"},
    {"title": "Basics of Value-Added Tax", "description": "Understand VAT principles, calculations, compliance requirements, and reporting obligations.", "code": "FIN-017"},
    {"title": "Core Excel Skills for Accountants and Financial Professionals", "description": "Essential Excel skills for financial analysis, reporting, and data management in accounting.", "code": "FIN-018"},
    {"title": "Top 25 Excel Formulas", "description": "Master the most important Excel formulas for financial calculations, analysis, and reporting.", "code": "FIN-019"}
]

async def seed_finance_courses():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Seeding 19 Finance courses...")
    
    for i, course_data in enumerate(FINANCE_COURSES, 1):
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
            "category": "FINANCE",
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
    
    print("\n✅ All Finance courses seeded!")
    client.close()

def get_lesson_title(page_num):
    titles = ["Introduction", "Key Concepts", "Principles", "Standards", "Regulations", "Planning", "Operations", "Analysis", "Technology", "Metrics", "Risk Management", "Quality Control", "Cost Management", "Performance", "Stakeholders", "Communication", "Problem Solving", "Decision Making", "Implementation", "Change Management", "Collaboration", "Leadership", "Improvement", "Case Studies", "Applications", "Challenges", "Solutions", "Trends", "Summary", "Next Steps"]
    return titles[page_num - 1] if page_num <= len(titles) else f"Topic {page_num}"

def generate_lesson_content(page_num, course_title):
    return f"""<div class="lesson-content">
<h2>{get_lesson_title(page_num)}</h2>
<p>Welcome to page {page_num} of <strong>{course_title}</strong>. This lesson provides essential financial knowledge for Flowitec professionals.</p>

<h3>Learning Objectives</h3>
<div class="highlight-box">
<ul>
<li>Understand key financial concepts and principles</li>
<li>Apply accounting standards in daily operations</li>
<li>Improve financial decision-making at Flowitec</li>
<li>Ensure compliance with financial regulations</li>
</ul>
</div>

<h3>Key Concepts</h3>
<p>Financial management is crucial for Flowitec's success in the pumps and valves industry. Sound financial practices ensure profitability, compliance, and sustainable growth.</p>

<div class="responsibilities-grid">
<div class="resp-card">
<h4>Financial Planning</h4>
<p>Strategic financial planning aligns resources with business objectives.</p>
<ul><li>Budgeting</li><li>Forecasting</li><li>Resource allocation</li></ul>
</div>
<div class="resp-card">
<h4>Accounting Operations</h4>
<p>Accurate accounting ensures financial integrity and compliance.</p>
<ul><li>Transaction recording</li><li>Financial reporting</li><li>Reconciliation</li></ul>
</div>
<div class="resp-card">
<h4>Financial Analysis</h4>
<p>Analysis provides insights for informed decision-making.</p>
<ul><li>Ratio analysis</li><li>Trend analysis</li><li>Performance metrics</li></ul>
</div>
<div class="resp-card">
<h4>Compliance & Control</h4>
<p>Strong controls protect assets and ensure regulatory compliance.</p>
<ul><li>Internal controls</li><li>Audit procedures</li><li>Risk management</li></ul>
</div>
</div>

<h3>Practical Application</h3>
<table>
<tr><th>Area</th><th>Challenge</th><th>Solution</th></tr>
<tr><td>Cash Flow</td><td>Managing liquidity</td><td>Cash flow forecasting and working capital management</td></tr>
<tr><td>Costing</td><td>Product pricing</td><td>Accurate cost accounting and margin analysis</td></tr>
<tr><td>Reporting</td><td>Timely information</td><td>Automated reporting systems and dashboards</td></tr>
<tr><td>Compliance</td><td>Regulatory changes</td><td>Continuous training and system updates</td></tr>
</table>

<h3>Best Practices</h3>
<div class="info-box">
<h4>Flowitec Financial Standards</h4>
<ul>
<li><strong>Accuracy:</strong> Ensure all financial data is accurate and complete</li>
<li><strong>Timeliness:</strong> Process transactions and reports promptly</li>
<li><strong>Compliance:</strong> Follow all accounting standards and regulations</li>
<li><strong>Transparency:</strong> Maintain clear and honest financial communication</li>
<li><strong>Efficiency:</strong> Optimize financial processes and controls</li>
</ul>
</div>

<h3>Case Study</h3>
<div class="example-box">
<p><strong>Situation:</strong> Flowitec needed to improve cash flow management to support expansion.</p>
<p><strong>Approach:</strong></p>
<ul>
<li>Implemented cash flow forecasting system</li>
<li>Optimized accounts receivable collection</li>
<li>Negotiated better payment terms with suppliers</li>
<li>Improved inventory management</li>
</ul>
<p><strong>Result:</strong> 25% improvement in cash flow, enabling strategic investments in growth.</p>
</div>

<div class="highlight-box">
<h4>Key Takeaway</h4>
<p>Strong financial management is essential for Flowitec's success. Apply these principles to contribute to the company's financial health and growth.</p>
</div>
</div>"""

def generate_quiz_questions():
    return [
        {"question": "What is the accounting equation?", "question_type": "multiple_choice", "options": ["Assets = Liabilities + Equity", "Revenue - Expenses = Profit", "Debits = Credits", "Income = Cash"], "correct_answer": "Assets = Liabilities + Equity", "points": 1, "order": 0},
        {"question": "Double-entry bookkeeping requires two entries for each transaction.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 1},
        {"question": "What does GAAP stand for?", "question_type": "multiple_choice", "options": ["Generally Accepted Accounting Principles", "Global Accounting and Auditing Practices", "General Asset Allocation Plan", "Government Approved Accounting Procedures"], "correct_answer": "Generally Accepted Accounting Principles", "points": 1, "order": 2},
        {"question": "Which financial statement shows profitability?", "question_type": "multiple_choice", "options": ["Balance Sheet", "Income Statement", "Cash Flow Statement", "Statement of Changes"], "correct_answer": "Income Statement", "points": 1, "order": 3},
        {"question": "Accounts receivable represents money owed to the company.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 4},
        {"question": "What is the purpose of variance analysis?", "question_type": "multiple_choice", "options": ["Compare actual vs budget", "Calculate taxes", "Record transactions", "Prepare statements"], "correct_answer": "Compare actual vs budget", "points": 1, "order": 5},
        {"question": "Internal controls help prevent fraud and errors.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 6},
        {"question": "What is working capital?", "question_type": "multiple_choice", "options": ["Total assets", "Current assets minus current liabilities", "Total revenue", "Net profit"], "correct_answer": "Current assets minus current liabilities", "points": 1, "order": 7},
        {"question": "Financial ratios help analyze company performance.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 8},
        {"question": "What is the purpose of budgeting?", "question_type": "multiple_choice", "options": ["Plan and control finances", "Record history", "Calculate taxes", "Audit accounts"], "correct_answer": "Plan and control finances", "points": 1, "order": 9},
        {"question": "Depreciation allocates asset cost over its useful life.", "question_type": "true_false", "options": ["True", "False"], "correct_answer": "True", "points": 1, "order": 10},
        {"question": "Which document shows cash inflows and outflows?", "question_type": "multiple_choice", "options": ["Income Statement", "Balance Sheet", "Cash Flow Statement", "Trial Balance"], "correct_answer": "Cash Flow Statement", "points": 1, "order": 11}
    ]

if __name__ == "__main__":
    asyncio.run(seed_finance_courses())
