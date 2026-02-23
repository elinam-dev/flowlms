import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def create_all_courses():
    courses_data = {
        "sales": [
            "Customer service skills",
            "B2B Customer success management",
            "Customer care skills and telephone etiquette",
            "Diploma in sales management",
            "B2B partnership development",
            "Mastering influence and Negotiation",
            "Marketing management - Capturing Marketing insights",
            "Introduction to marketing management",
            "Mastering influence in sales",
            "Sales techniques - interacting with customers",
            "Sales and Negotiation skills",
            "Understanding key account management",
            "Understanding market demand, branding and communications",
            "Effective sales skills",
            "Sales techniques - using competitive sales strategies",
            "B2B lead Generation techniques",
            "Advanced B2B marketing strategies"
        ],
        "supply_chain": [
            "Diploma in supply chain management",
            "Understanding supply chain risk management",
            "B2B supply chain management",
            "Understanding supply chain ecosystem fundamentals of using six sigma in supply chain",
            "International marketing and supply chain management",
            "Freight broker training",
            "The complete guide to sea export forwarding",
            "Warehouse management: principles, trends and processes",
            "Lean six sigma:white belt"
        ],
        "health_safety": [
            "Health and safety well-being - Mental Health",
            "Fundamentals of health and safety in the workplace",
            "Health and safety - personal protective equipment"
        ],
        "finance": [
            "Fundamentals of accounting",
            "Diploma in financial accounting",
            "Introduction to business accounting",
            "Essentials of throughout accounting and lean accounting",
            "Diploma in cost accounting",
            "Sage One - Bookkeeping and accounting",
            "The accounting cycle and financial statements",
            "Master the double-entry accounting system",
            "Tax accounting systems and administration",
            "Financial statement analysis: accounting ratios and analytical strategy",
            "Cost and management accounting: Planning for effective strategy execution",
            "Diploma in decision making using financial accounting",
            "Accounts receive able management",
            "Accounts payable management",
            "Fundamentals of budgeting and variance analysis",
            "Essentials of SAP CO - managing and controlling cost",
            "Basics of value-Added tax",
            "Core excel skills for accountants and financial professionals",
            "Top 25 excel formulas"
        ],
        "hr": [
            "Introduction to modern human resource management",
            "Human Resource systems and processes",
            "Diploma in introduction to human resource concepts",
            "HR Analytics - Harnessing HR Data for organization success",
            "Modern Human Resource Management - Recruitment and selection process",
            "Human Resource policies and organization structure",
            "Onboarding principles for employees",
            "Human Resources: Employee Management and Training",
            "Diploma in strategic HR",
            "HR: Talent Management and Workforce Development",
            "HRM - the ultimate employee onboarding guide with 4Cs",
            "Respect foundations: Diversity, respect, and substance Abuse in workplace",
            "Human Resources: Discipline and termination",
            "Competency Mapping in HR: Transform people into Human capital",
            "Mastering HR Budget: Strategic financial planning for professionals",
            "Employee onboarding and motivation",
            "Facility management- maintenance and repairs",
            "Diploma in strategic performance management"
        ],
        "management": [
            "Employee Management for Business Mangers",
            "Leadership and management for managers",
            "Diploma in management for New managers",
            "Effective communication skills for Managers",
            "Line management essential skills and concepts",
            "Executive strategy and management",
            "Conflict management and resolution"
        ],
        "engineering": [
            "Mechanical engineering and design concepts",
            "Diploma in laws of thermodynamics",
            "Diploma in mechatronics",
            "Marine auxiliary machinery - pumps, fans and blowers"
        ],
        "personal_branding": [
            "Personal branding for professionals",
            "Telephone etiquette for personal assistants"
        ],
        "general": [
            "How to design performance management system",
            "Behavioral interviewing techniques for Employers"
        ]
    }
    
    created_count = 0
    
    for category, course_titles in courses_data.items():
        for title in course_titles:
            # Skip if course already exists
            existing = db.courses.find_one({"title": title})
            if existing:
                print(f"Skipping existing course: {title}")
                continue
                
            course_id = str(uuid.uuid4())
            
            # Create course
            course_doc = {
                "id": course_id,
                "title": title,
                "description": f"Professional training course in {title.lower()}",
                "thumbnail": "/images/course-thumbnail.jpg",
                "category": category,
                "duration_hours": 2,
                "is_published": True,
                "course_type": "optional",
                "enrolled_users": [],
                "created_at": datetime.now().isoformat()
            }
            
            db.courses.insert_one(course_doc)
            
            # Create module
            module_id = f"{course_id}_module_1"
            module_doc = {
                "id": module_id,
                "course_id": course_id,
                "title": "Course Content",
                "description": f"Main content for {title}",
                "order": 0
            }
            
            db.modules.insert_one(module_doc)
            
            # Create basic lesson
            lesson_doc = {
                "id": f"{module_id}_lesson_1",
                "module_id": module_id,
                "title": "Introduction",
                "content_type": "text",
                "content": f'<div class="lesson-content"><h2>{title}</h2><p>Welcome to this comprehensive course on {title.lower()}. This course will provide you with essential knowledge and skills.</p></div>',
                "duration_minutes": 30,
                "order": 0
            }
            
            db.lessons.insert_one(lesson_doc)
            created_count += 1
    
    print(f"Created {created_count} new courses")

if __name__ == "__main__":
    create_all_courses()