"""
Check all courses and add missing quizzes
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

QUIZ_QUESTIONS = {
    "SALES": [
        {"question": "What is the first step in the sales process?", "type": "multiple_choice", "options": ["Prospecting", "Closing", "Follow-up", "Presentation"], "correct_answer": "Prospecting"},
        {"question": "Active listening is crucial in sales.", "type": "true_false", "correct_answer": "true"},
        {"question": "What does CRM stand for?", "type": "short_answer", "correct_answer": "Customer Relationship Management"},
        {"question": "Which technique helps overcome objections?", "type": "multiple_choice", "options": ["Ignoring them", "Acknowledging and addressing", "Arguing", "Changing topic"], "correct_answer": "Acknowledging and addressing"},
        {"question": "What is a key metric in sales performance?", "type": "short_answer", "correct_answer": "Conversion rate"},
        {"question": "Building rapport with customers increases sales success.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is upselling?", "type": "multiple_choice", "options": ["Selling more expensive products", "Selling additional products", "Discounting products", "Returning products"], "correct_answer": "Selling more expensive products"},
        {"question": "Follow-up after a sale is unnecessary.", "type": "true_false", "correct_answer": "false"},
        {"question": "What is a sales pipeline?", "type": "short_answer", "correct_answer": "Visual representation of sales process stages"},
        {"question": "Which closing technique asks for the sale directly?", "type": "multiple_choice", "options": ["Direct close", "Assumptive close", "Alternative close", "Summary close"], "correct_answer": "Direct close"},
        {"question": "Value proposition explains why customers should buy.", "type": "true_false", "correct_answer": "true"},
        {"question": "What does B2B stand for?", "type": "short_answer", "correct_answer": "Business to Business"}
    ],
    "SUPPLY CHAIN": [
        {"question": "What is the main goal of supply chain management?", "type": "multiple_choice", "options": ["Cost reduction", "Customer satisfaction", "Efficiency and value", "Speed"], "correct_answer": "Efficiency and value"},
        {"question": "Just-in-time inventory reduces storage costs.", "type": "true_false", "correct_answer": "true"},
        {"question": "What does EOQ stand for?", "type": "short_answer", "correct_answer": "Economic Order Quantity"},
        {"question": "Which is a supply chain risk?", "type": "multiple_choice", "options": ["Supplier failure", "High profits", "Customer loyalty", "Low costs"], "correct_answer": "Supplier failure"},
        {"question": "What is lead time?", "type": "short_answer", "correct_answer": "Time from order to delivery"},
        {"question": "Lean principles eliminate waste.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is the bullwhip effect?", "type": "multiple_choice", "options": ["Demand amplification", "Cost reduction", "Quality improvement", "Speed increase"], "correct_answer": "Demand amplification"},
        {"question": "Forecasting is unnecessary in supply chain.", "type": "true_false", "correct_answer": "false"},
        {"question": "What does SKU stand for?", "type": "short_answer", "correct_answer": "Stock Keeping Unit"},
        {"question": "Which technology improves supply chain visibility?", "type": "multiple_choice", "options": ["IoT sensors", "Paper records", "Manual tracking", "Phone calls"], "correct_answer": "IoT sensors"},
        {"question": "Vendor relationships impact supply chain success.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is reverse logistics?", "type": "short_answer", "correct_answer": "Managing product returns and recycling"}
    ],
    "FINANCE": [
        {"question": "What are the three main financial statements?", "type": "multiple_choice", "options": ["Balance sheet, income statement, cash flow", "Budget, forecast, report", "Assets, liabilities, equity", "Revenue, expenses, profit"], "correct_answer": "Balance sheet, income statement, cash flow"},
        {"question": "Assets equal liabilities plus equity.", "type": "true_false", "correct_answer": "true"},
        {"question": "What does ROI stand for?", "type": "short_answer", "correct_answer": "Return on Investment"},
        {"question": "Which measures profitability?", "type": "multiple_choice", "options": ["Net profit margin", "Current ratio", "Debt ratio", "Asset turnover"], "correct_answer": "Net profit margin"},
        {"question": "What is working capital?", "type": "short_answer", "correct_answer": "Current assets minus current liabilities"},
        {"question": "Depreciation is a cash expense.", "type": "true_false", "correct_answer": "false"},
        {"question": "What does EBITDA stand for?", "type": "multiple_choice", "options": ["Earnings before interest, taxes, depreciation, amortization", "Equity before income and debt", "Expenses before income", "None"], "correct_answer": "Earnings before interest, taxes, depreciation, amortization"},
        {"question": "Cash flow and profit are the same.", "type": "true_false", "correct_answer": "false"},
        {"question": "What is the current ratio?", "type": "short_answer", "correct_answer": "Current assets divided by current liabilities"},
        {"question": "Which statement shows financial position?", "type": "multiple_choice", "options": ["Balance sheet", "Income statement", "Cash flow statement", "Budget"], "correct_answer": "Balance sheet"},
        {"question": "Internal controls prevent fraud.", "type": "true_false", "correct_answer": "true"},
        {"question": "What does NPV stand for?", "type": "short_answer", "correct_answer": "Net Present Value"}
    ],
    "HUMAN RESOURCES": [
        {"question": "What is the primary goal of HR?", "type": "multiple_choice", "options": ["Manage people effectively", "Reduce costs", "Hire quickly", "Fire employees"], "correct_answer": "Manage people effectively"},
        {"question": "Diversity improves organizational performance.", "type": "true_false", "correct_answer": "true"},
        {"question": "What does KPI stand for?", "type": "short_answer", "correct_answer": "Key Performance Indicator"},
        {"question": "Which is part of total compensation?", "type": "multiple_choice", "options": ["Salary and benefits", "Only salary", "Only bonuses", "Only insurance"], "correct_answer": "Salary and benefits"},
        {"question": "What is employee engagement?", "type": "short_answer", "correct_answer": "Emotional commitment to organization"},
        {"question": "Performance reviews should be annual only.", "type": "true_false", "correct_answer": "false"},
        {"question": "What is succession planning?", "type": "multiple_choice", "options": ["Preparing future leaders", "Firing employees", "Hiring externally", "Reducing staff"], "correct_answer": "Preparing future leaders"},
        {"question": "Training is an expense, not investment.", "type": "true_false", "correct_answer": "false"},
        {"question": "What does HRIS stand for?", "type": "short_answer", "correct_answer": "Human Resource Information System"},
        {"question": "Which law protects against discrimination?", "type": "multiple_choice", "options": ["Equal Employment Opportunity", "Tax law", "Contract law", "Property law"], "correct_answer": "Equal Employment Opportunity"},
        {"question": "Exit interviews provide valuable feedback.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is onboarding?", "type": "short_answer", "correct_answer": "Process of integrating new employees"}
    ],
    "MANAGEMENT": [
        {"question": "What are the four functions of management?", "type": "multiple_choice", "options": ["Planning, organizing, leading, controlling", "Hiring, firing, training, paying", "Selling, buying, making, shipping", "None"], "correct_answer": "Planning, organizing, leading, controlling"},
        {"question": "Delegation empowers team members.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is emotional intelligence?", "type": "short_answer", "correct_answer": "Ability to understand and manage emotions"},
        {"question": "Which leadership style involves team participation?", "type": "multiple_choice", "options": ["Democratic", "Autocratic", "Laissez-faire", "Transactional"], "correct_answer": "Democratic"},
        {"question": "What does SMART stand for in goal setting?", "type": "short_answer", "correct_answer": "Specific, Measurable, Achievable, Relevant, Time-bound"},
        {"question": "Micromanagement increases productivity.", "type": "true_false", "correct_answer": "false"},
        {"question": "What is change management?", "type": "multiple_choice", "options": ["Managing organizational transitions", "Changing managers", "Modifying products", "Altering prices"], "correct_answer": "Managing organizational transitions"},
        {"question": "Feedback should only be negative.", "type": "true_false", "correct_answer": "false"},
        {"question": "What is servant leadership?", "type": "short_answer", "correct_answer": "Leading by serving others"},
        {"question": "Which resolves team conflicts best?", "type": "multiple_choice", "options": ["Open communication", "Ignoring issues", "Taking sides", "Avoiding discussion"], "correct_answer": "Open communication"},
        {"question": "Strategic planning sets long-term direction.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is accountability?", "type": "short_answer", "correct_answer": "Taking responsibility for actions and results"}
    ],
    "DEFAULT": [
        {"question": "What is the main topic of this course?", "type": "short_answer", "correct_answer": "Course subject matter"},
        {"question": "Continuous learning improves professional skills.", "type": "true_false", "correct_answer": "true"},
        {"question": "Which is most important for success?", "type": "multiple_choice", "options": ["Knowledge and application", "Luck", "Connections", "Timing"], "correct_answer": "Knowledge and application"},
        {"question": "What does best practice mean?", "type": "short_answer", "correct_answer": "Most effective method or technique"},
        {"question": "Compliance with regulations is mandatory.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is quality assurance?", "type": "multiple_choice", "options": ["Ensuring standards are met", "Reducing costs", "Increasing speed", "Hiring staff"], "correct_answer": "Ensuring standards are met"},
        {"question": "Documentation is unnecessary if you remember.", "type": "true_false", "correct_answer": "false"},
        {"question": "What is continuous improvement?", "type": "short_answer", "correct_answer": "Ongoing effort to enhance processes"},
        {"question": "Which approach solves problems effectively?", "type": "multiple_choice", "options": ["Systematic analysis", "Guessing", "Ignoring", "Blaming"], "correct_answer": "Systematic analysis"},
        {"question": "Teamwork enhances results.", "type": "true_false", "correct_answer": "true"},
        {"question": "What is a stakeholder?", "type": "short_answer", "correct_answer": "Person or group with interest in outcome"},
        {"question": "Ethics should guide all decisions.", "type": "true_false", "correct_answer": "true"}
    ]
}

async def fix_missing_quizzes():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    courses = await db.courses.find({}).to_list(None)
    print(f"Checking {len(courses)} courses for missing quizzes...\n")
    
    missing_count = 0
    
    for idx, course in enumerate(courses, 1):
        course_id = course['id']
        title = course['title']
        category = course.get('category', 'DEFAULT')
        
        module = await db.modules.find_one({"course_id": course_id})
        if not module:
            continue
        
        module_id = module['id']
        quiz = await db.quizzes.find_one({"module_id": module_id})
        
        if not quiz:
            missing_count += 1
            questions = QUIZ_QUESTIONS.get(category, QUIZ_QUESTIONS["DEFAULT"])
            
            quiz_id = str(uuid.uuid4())
            await db.quizzes.insert_one({
                "id": quiz_id,
                "module_id": module_id,
                "title": f"{title} - Final Assessment",
                "description": f"Test your knowledge of {title}. You need 70% to pass.",
                "passing_score": 70,
                "questions": questions,
                "time_limit_minutes": 24,
                "created_at": "2024-01-01T00:00:00"
            })
            print(f"  ✓ {idx}. Added quiz to: {title}")
        else:
            print(f"  - {idx}. {title} - Already has quiz")
    
    print(f"\n✅ Added {missing_count} missing quizzes!")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_missing_quizzes())
