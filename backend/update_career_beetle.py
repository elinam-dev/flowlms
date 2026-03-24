import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def update():
    await db.career_beetle.delete_many({})
    await db.career_beetle.insert_one({
        "departments": [
            {
                "id": "sales", "name": "SALES DEPARTMENT",
                "roles": [
                    {"id": "mech_sales_trainee", "title": "Mechanical Sales Engineer Trainee", "level": "Entry level", "key_skills": "Technical knowledge, CRM basics, communication", "qualifications": "First Degree", "timeline": "3-6 months", "focus": "Learn products, shadow sales calls and meetings, understand client needs"},
                    {"id": "mech_sales_assoc", "title": "Mechanical Sales Engineer Associate", "level": "Intermediate", "key_skills": "Product knowledge, customer service", "qualifications": "First Degree", "timeline": "1-2 years", "focus": "Support sales cycle, build client relationships, handle proposals"},
                    {"id": "sr_mech_sales", "title": "Senior Mechanical Sales Engineer", "level": "Mid level", "key_skills": "Solutions selling, competitor strategies, technical advisory, leadership", "qualifications": "First Degree, sales training/related certifications", "timeline": "2-4 years", "focus": "Manage accounts, lead technical sales presentations, close deals"},
                    {"id": "country_sales_mgr", "title": "Country Sales Manager", "level": "First Level", "key_skills": "Leadership, sales strategy, business development, key account management", "qualifications": "First Degree / Master's / related certification", "timeline": "5-6 years", "focus": "Lead teams, drive revenue strategy, mentor junior engineers"},
                    {"id": "regional_head_sales", "title": "Regional Head of Sales", "level": "Senior Mgt.", "key_skills": "Sales strategy, market analysis, performance analysis", "qualifications": "First Degree / Master's / related certification", "timeline": "7+ years", "focus": "Lead regional team, drive revenue across region"},
                    {"id": "group_tech_sales_mgr", "title": "Group Technical Sales Manager", "level": "Senior Mgt.", "key_skills": "Leadership, sales strategy, business development, key account management", "qualifications": "First Degree / Master's / related certification", "timeline": "7+ years", "focus": "Lead teams, drive revenue, mentor engineers"},
                    {"id": "vp_sales", "title": "VP Sales", "level": "Senior Level", "key_skills": "Strategic thinking, communication, results-driven", "qualifications": "First Degree / Master's / related certification", "timeline": "8+ years", "focus": "Visionary leadership, talent development, budget management"}
                ]
            },
            {
                "id": "supply_chain", "name": "SUPPLY CHAIN DEPARTMENT",
                "roles": [
                    {"id": "sales_admin", "title": "Sales Administrator", "level": "Entry level", "key_skills": "Basic sales & procurement knowledge", "qualifications": "First Degree / HND", "timeline": "0-1 year", "focus": "Support procurement/logistics, manage inventory workflows"},
                    {"id": "supply_chain_off", "title": "Supply Chain Officer", "level": "Intermediate", "key_skills": "Inventory control, procurement basics, reporting & forecasting", "qualifications": "First Degree", "timeline": "1-2 years", "focus": "Analyze supply chain data, optimize processes"},
                    {"id": "sr_supply_chain_off", "title": "Senior Supply Chain Officer", "level": "Mid level", "key_skills": "Advanced Excel, project management, communication", "qualifications": "First Degree / certifications", "timeline": "2-4 years", "focus": "Manage teams, lead initiatives and budgeting"},
                    {"id": "supply_chain_mgr", "title": "Supply Chain Manager", "level": "First Level", "key_skills": "Leadership, strategic sourcing, risk management, negotiation", "qualifications": "First Degree / Master's / certifications", "timeline": "5-6 years", "focus": "Strategy, innovation, operations"},
                    {"id": "head_supply_chain", "title": "Head of Supply Chain", "level": "Senior Mgt.", "key_skills": "Executive decision-making, logistics, digital transformation", "qualifications": "First Degree / Master's / certifications", "timeline": "7+ years", "focus": "Drive innovation, lead team, develop strategies"},
                    {"id": "group_supply_chain_mgr", "title": "Group Supply Chain Manager", "level": "Senior Mgt.", "key_skills": "Leadership, sourcing strategy", "qualifications": "First Degree / Master's / certifications", "timeline": "8+ years", "focus": "Group leadership, strategic direction"},
                    {"id": "coo_supply_chain", "title": "COO – Supply Chain", "level": "Senior Level", "key_skills": "Strategic thinking, communication, results-driven", "qualifications": "First Degree / Master's / certifications", "timeline": "8+ years", "focus": "Visionary leadership, procurement & supply chain strategy"}
                ]
            },
            {
                "id": "finance", "name": "FINANCE DEPARTMENT",
                "roles": [
                    {"id": "accounts_clerk", "title": "Accounts Clerk", "level": "Entry level", "key_skills": "Accounting basics, Excel, attention to detail", "qualifications": "First Degree / HND", "timeline": "0-1 year", "focus": "Learn fundamentals, system familiarization"},
                    {"id": "finance_off", "title": "Finance Officer", "level": "Intermediate", "key_skills": "Reporting, budgeting, forecasting, collaboration", "qualifications": "First Degree", "timeline": "2-4 years", "focus": "Tax filings, debt collection, specialization"},
                    {"id": "accountant", "title": "Accountant", "level": "Mid level", "key_skills": "Financial modeling, coordination, compliance", "qualifications": "First Degree / Chartered Certification", "timeline": "5-6 years", "focus": "Leadership transition, process improvement"},
                    {"id": "finance_mgr", "title": "Finance Manager", "level": "First Level", "key_skills": "Strategic planning, risk & compliance leadership", "qualifications": "First Degree / Chartered Certification", "timeline": "7+ years", "focus": "Strategy, business alignment"},
                    {"id": "group_finance_mgr", "title": "Group Finance Manager", "level": "Senior Mgt.", "key_skills": "Analytical thinking, strategic finance expertise", "qualifications": "First Degree / Chartered / Master's", "timeline": "8+ years", "focus": "Forecasting, compliance, financial strategy"},
                    {"id": "cfo", "title": "CFO", "level": "Senior Level", "key_skills": "Strategic planning, compliance leadership", "qualifications": "First Degree / Chartered / Master's", "timeline": "9+ years", "focus": "Financial planning, investor relations, risk management"}
                ]
            },
            {
                "id": "hr", "name": "HR DEPARTMENT",
                "roles": [
                    {"id": "hr_assistant", "title": "HR Assistant/Admin", "level": "Entry level", "key_skills": "HRIS, record keeping, policy understanding", "qualifications": "First Degree / HND", "timeline": "0-1 year", "focus": "Learn HR operations and systems"},
                    {"id": "hr_off", "title": "HR Officer / Generalist", "level": "Intermediate", "key_skills": "Recruitment, onboarding, benefits, employee relations", "qualifications": "First Degree", "timeline": "1-3 years", "focus": "Manage HR tasks, develop specialization"},
                    {"id": "hr_mgr", "title": "HR Manager", "level": "Mid level", "key_skills": "Talent management, HR analytics, compliance", "qualifications": "First Degree / HR certification", "timeline": "3-5 years", "focus": "Lead initiatives, advise teams"},
                    {"id": "hr_bp", "title": "HR Business Partner / HR Lead", "level": "First Level", "key_skills": "Workforce planning, coaching, succession planning", "qualifications": "First Degree / CIHRM / SHRP", "timeline": "6+ years", "focus": "Strategy, leadership, organizational growth"},
                    {"id": "chief_hr", "title": "Chief HR Director", "level": "Senior Level", "key_skills": "Strategic thinking, leadership, business acumen", "qualifications": "First Degree / CIHRM / SHRP", "timeline": "7+ years", "focus": "Talent strategy, HR leadership"}
                ]
            },
            {
                "id": "facilities_a", "name": "FACILITIES DEPARTMENT A",
                "roles": [
                    {"id": "pool_driver", "title": "Pool Driver", "level": "Entry level", "key_skills": "Vehicle maintenance, safety, route optimization", "qualifications": "Diploma / HND", "timeline": "2-4 years", "focus": "Driving, logistics support"},
                    {"id": "sr_driver", "title": "Senior Driver", "level": "Mid level", "key_skills": "Supervision, route planning, compliance", "qualifications": "Diploma / HND / Degree", "timeline": "4+ years", "focus": "Defensive driving, leadership"},
                    {"id": "chief_driver", "title": "Chief Driver", "level": "First Level", "key_skills": "Supervision, planning, compliance", "qualifications": "Diploma / HND / Degree", "timeline": "6+ years", "focus": "Team leadership"}
                ]
            },
            {
                "id": "facilities_b", "name": "FACILITIES DEPARTMENT B",
                "roles": [
                    {"id": "office_assistant", "title": "Office Assistant / Coordinator", "level": "Entry level", "key_skills": "Office supplies, maintenance support", "qualifications": "Diploma / HND", "timeline": "1-2 years", "focus": "Daily operations, support facility needs"},
                    {"id": "office_mgr", "title": "Office Manager", "level": "Mid level", "key_skills": "Leadership, general maintenance", "qualifications": "Diploma / HND / Degree", "timeline": "3-4 years", "focus": "Efficiency, oversee operations"},
                    {"id": "facilities_mgr", "title": "Facilities Manager", "level": "First Level", "key_skills": "Facilities strategy, health & safety, space planning", "qualifications": "Diploma / HND / Degree", "timeline": "5+ years", "focus": "Safety, long-term planning"}
                ]
            }
        ]
    })
    print("Career Beetle updated successfully!")
    client.close()

asyncio.run(update())
