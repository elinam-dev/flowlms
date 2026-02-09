import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def update_career_beetle():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    await db.career_beetle.delete_many({})
    await db.career_beetle.insert_one({
        "departments": [
            {"id": "sales", "name": "SALES DEPARTMENT", "roles": [
                {"id": "mech_sales_trainee", "title": "Mechanical Sales Engineer Trainee", "level": "Entry level", "key_skills": "Technical Knowledge, CRM basics, Communication", "qualifications": "First Degree", "timeline": "3-6 months", "focus": "Learn products, shadow sales calls and meetings, understand client needs"},
                {"id": "mech_sales_assoc", "title": "Mechanical Sales Engineer Associate", "level": "Intermediate", "key_skills": "Product knowledge, customer service", "qualifications": "First Degree", "timeline": "1-2 years", "focus": "Support sales cycle, build client relationships, handle proposals"},
                {"id": "sr_mech_sales", "title": "Senior Mechanical Sales Engineer", "level": "Mid level", "key_skills": "Solutions sharing, competitor unseating strategies, technical advisory, leadership", "qualifications": "First Degree, Sales trainings/related certifications", "timeline": "2-4 years", "focus": "Manage accounts, lead technical sales presentations, close deals"},
                {"id": "country_sales_mgr", "title": "Country Sales Manager", "level": "First Level", "key_skills": "Leadership, sales strategy, business development, key account mgt", "qualifications": "First degree/Masters Degree/related certification", "timeline": "5-6 years", "focus": "Lead teams, drive revenue strategy, mentor junior engineers"},
                {"id": "regional_head_sales", "title": "Regional Head of Sales", "level": "Senior Mgt.", "key_skills": "Sales strategy, market analysis, performance analysis", "qualifications": "First degree/Masters Degree/related certification", "timeline": "7+ years", "focus": "Leads regional team, drives revenue across region"},
                {"id": "group_tech_sales_mgr", "title": "Group Technical Sales Manager", "level": "Senior Mgt.", "key_skills": "Leadership, sales strategy, business development, key account mgt", "qualifications": "First degree/Masters Degree/related certification", "timeline": "7+ years", "focus": "Lead teams, drive revenue strategy, mentor junior engineers"},
                {"id": "vp_sales", "title": "VP Sales", "level": "Senior Level", "key_skills": "Strategic thinking, excellent communication skill, Results driven", "qualifications": "First degree/Masters Degree/related certification", "timeline": "8+ years", "focus": "Visionary leadership, talent development, budget management"}
            ]},
            {"id": "supply_chain", "name": "SUPPLY CHAIN DEPARTMENT", "roles": [
                {"id": "sales_admin", "title": "Sales Administrator", "level": "Entry level", "key_skills": "Basic sales and procurement knowledge", "qualifications": "First Degree/HND", "timeline": "0-1 year", "focus": "Support procurement and logistics, manage inventory workflows and vendor/client comms"},
                {"id": "supply_chain_off", "title": "Supply Chain Officer", "level": "Intermediate", "key_skills": "Inventory controls, procurement basics, reporting and forecasting", "qualifications": "First Degree", "timeline": "1-2 years", "focus": "Analyze supply chain data, optimize processes and lead small projects"},
                {"id": "sr_supply_chain_off", "title": "Senior Supply Chain Officer", "level": "Mid level", "key_skills": "Advanced excel, project management, good communication", "qualifications": "First Degree/Related certifications", "timeline": "2-4 years", "focus": "Manage teams and processes - Lead strategic initiatives and budgeting"},
                {"id": "supply_chain_mgr", "title": "Supply Chain Manager", "level": "First Level", "key_skills": "Leadership, strategic sourcing, risk management, contract negotiations", "qualifications": "First Degree/Masters Degree/Related Certifications", "timeline": "5-6 years", "focus": "Set vision and strategy - Drive innovation and group operations"},
                {"id": "head_supply_chain", "title": "Head of Supply Chain Dept.", "level": "Senior Mgt.", "key_skills": "Executive decision making, group logistics, digital transformation", "qualifications": "First Degree/Masters Degree/Related Certifications", "timeline": "7+ years", "focus": "Drive innovation, lead team and curate strong strategies"},
                {"id": "group_supply_chain_mgr", "title": "Group Supply Chain Manager", "level": "Senior Mgt.", "key_skills": "Leadership, sourcing strategy", "qualifications": "First Degree/Masters Degree/Related Certifications", "timeline": "8+ years", "focus": "Group leadership, curation of strong strategies, visionary leadership"},
                {"id": "coo_supply_chain", "title": "COO - Supply Chain", "level": "Senior Level", "key_skills": "Strategic thinking, excellent communication skill, Results driven", "qualifications": "First Degree/Masters Degree/Related Certifications", "timeline": "8+ years", "focus": "Visionary leadership, talent development, procurement and supply chain process management"}
            ]},
            {"id": "finance", "name": "FINANCE DEPARTMENT", "roles": [
                {"id": "accounts_clerk", "title": "Accounts Clerk", "level": "Entry level", "key_skills": "Basic accounting principles, use of Excel and other accounting tools, accuracy and attention to detail", "qualifications": "First Degree/HND", "timeline": "0-1 year", "focus": "Learning fundamentals, system familiarization"},
                {"id": "finance_off", "title": "Finance Officer", "level": "Intermediate", "key_skills": "Financial reporting, budgeting & forecasting, cross functional collaboration", "qualifications": "First Degree", "timeline": "2-4 years", "focus": "Execution of tasks (tax filings, debt collection etc.), early specialization"},
                {"id": "accountant", "title": "Accountant", "level": "Mid level", "key_skills": "Financial modeling, team coordination, regulatory and compliance", "qualifications": "First Degree/Chartered Certification", "timeline": "5-6 years", "focus": "Leadership transition, process optimization, mentorship"},
                {"id": "finance_mgr", "title": "Finance Manager", "level": "First Level", "key_skills": "Strategic planning - Risk & compliance leadership", "qualifications": "First Degree/Chartered Certification", "timeline": "7+ years", "focus": "Strategic leadership, business alignment & innovation"},
                {"id": "group_finance_mgr", "title": "Group Finance Manager", "level": "Senior Mgt.", "key_skills": "Analytical thinking, strategic thinking, financial expertise", "qualifications": "First Degree/Chartered Certification/Masters", "timeline": "8+ years", "focus": "Financial forecasting, compliance and risk management, strategic financial guidance"},
                {"id": "cfo", "title": "CFO", "level": "Senior Level", "key_skills": "Strategic planning - Risk & compliance leadership, strategic thinking", "qualifications": "First Degree/Chartered Certification/Masters/any other related certifications", "timeline": "9+ years", "focus": "Financial planning and forecasting, investor relation, risk management"}
            ]},
            {"id": "hr", "name": "HR DEPARTMENT", "roles": [
                {"id": "hr_assistant", "title": "HR Assistant/Admin", "level": "Entry level", "key_skills": "HRIS, record keeping, understanding of HR policies and procedures", "qualifications": "First Degree/HND", "timeline": "0-1 year", "focus": "Learning core HR operations and systems"},
                {"id": "hr_off", "title": "HR Officer/Generalist", "level": "Intermediate", "key_skills": "Recruitment & onboarding, benefits administration, employee relations basics", "qualifications": "First Degree", "timeline": "1-3 years", "focus": "Managing day-to-day HR tasks, developing core specialties"},
                {"id": "hr_mgr", "title": "HR Manager", "level": "Mid level", "key_skills": "Talent Management, policy development, HR analytics & Compliance", "qualifications": "First Degree/HR Professional certification", "timeline": "3-5 years", "focus": "Leading initiatives, advising teams, building programs"},
                {"id": "hr_bp", "title": "HR Business Partner/HR Lead", "level": "First Level", "key_skills": "Strategic workforce planning, leadership coaching, change management and succession planning", "qualifications": "First Degree/CIHRM/SHRP", "timeline": "6+ years", "focus": "Driving culture, strategy, leadership and organizational growth"},
                {"id": "chief_hr", "title": "Chief HR Director", "level": "Senior Level", "key_skills": "Strategic thinking, leadership skills, Business acumen", "qualifications": "First Degree/CIHRM/SHRP", "timeline": "7+ years", "focus": "Leadership development, talent management, HR Strategy"}
            ]},
            {"id": "facilities_a", "name": "FACILITIES DEPARTMENT A", "roles": [
                {"id": "pool_driver", "title": "Pool Driver", "level": "Entry level", "key_skills": "Vehicle maintenance, road safety and company policies, route optimization", "qualifications": "Diploma/HND", "timeline": "2-4 years", "focus": "Basic driving skills, long distance driving"},
                {"id": "sr_driver", "title": "Senior Driver", "level": "Mid level", "key_skills": "Team supervisor, route planning, fleet compliance", "qualifications": "Diploma/HND/First Degree", "timeline": "4+ years", "focus": "Defensive driving, team leadership"},
                {"id": "chief_driver", "title": "Chief Driver", "level": "First Level", "key_skills": "Team supervisor, route planning, fleet compliance", "qualifications": "Diploma/HND/First Degree", "timeline": "6+ years", "focus": "Defensive driving, team leadership"}
            ]},
            {"id": "facilities_b", "name": "FACILITIES DEPARTMENT B", "roles": [
                {"id": "office_assistant", "title": "Office Assistant/Coordinator", "level": "Entry level", "key_skills": "Basic office supplies stocking, maintaining functioning devices etc.", "qualifications": "Diploma/HND", "timeline": "1-2 years", "focus": "Managing day-to-day operations and supporting facility needs"},
                {"id": "office_mgr", "title": "Office Manager", "level": "Mid level", "key_skills": "Team leadership, General maintenance", "qualifications": "Diploma/HND/First Degree", "timeline": "3-4 years", "focus": "Improving efficiency and overseeing office operations"},
                {"id": "facilities_mgr", "title": "Facilities Manager", "level": "First Level", "key_skills": "Facilities strategy, health and safety compliance, office space planning", "qualifications": "Diploma/HND/First Degree", "timeline": "5+ years", "focus": "Leading office safety, and long-term facility planning"}
            ]}
        ]
    })
    
    print("Career Beetle data updated successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(update_career_beetle())
