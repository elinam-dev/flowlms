import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Facility management is defined as:",
        "options": ["Managing only the cleaning and security of a building", "The integrated management of people, place and process to ensure the built environment supports the core business objectives", "Managing only capital construction projects", "The financial management of property assets"],
        "correct_answer": "The integrated management of people, place and process to ensure the built environment supports the core business objectives"
    },
    {
        "question": "Preventive maintenance in facility management involves:",
        "options": ["Repairing equipment only after it breaks down", "Scheduled, routine maintenance activities carried out to prevent equipment failure and extend asset life", "Replacing all equipment on a fixed annual schedule", "Outsourcing all maintenance to external contractors"],
        "correct_answer": "Scheduled, routine maintenance activities carried out to prevent equipment failure and extend asset life"
    },
    {
        "question": "Corrective maintenance refers to:",
        "options": ["Maintenance carried out before a fault occurs", "Maintenance performed to restore a failed or malfunctioning asset to its operational condition", "Routine cleaning and housekeeping activities", "Planned upgrades to building systems"],
        "correct_answer": "Maintenance performed to restore a failed or malfunctioning asset to its operational condition"
    },
    {
        "question": "Predictive maintenance uses:",
        "options": ["Fixed maintenance schedules regardless of equipment condition", "Data and condition monitoring tools to predict when equipment is likely to fail, enabling maintenance before breakdown occurs", "Only visual inspections by maintenance staff", "Manufacturer recommendations as the sole guide"],
        "correct_answer": "Data and condition monitoring tools to predict when equipment is likely to fail, enabling maintenance before breakdown occurs"
    },
    {
        "question": "A Computerised Maintenance Management System (CMMS) is used to:",
        "options": ["Manage employee payroll in the facilities team", "Plan, track and manage maintenance activities, work orders, asset records and maintenance history", "Design new building layouts", "Process supplier invoices only"],
        "correct_answer": "Plan, track and manage maintenance activities, work orders, asset records and maintenance history"
    },
    {
        "question": "The primary goal of an asset management strategy in facility management is to:",
        "options": ["Maximise the number of assets owned by the organisation", "Optimise the performance, cost and lifecycle of physical assets to support business operations", "Replace all assets every five years", "Minimise the facilities management team's headcount"],
        "correct_answer": "Optimise the performance, cost and lifecycle of physical assets to support business operations"
    },
    {
        "question": "A work order in facility management is:",
        "options": ["A purchase order for new equipment", "A formal document authorising and tracking a specific maintenance or repair task", "An employee performance review form", "A building permit from the local authority"],
        "correct_answer": "A formal document authorising and tracking a specific maintenance or repair task"
    },
    {
        "question": "Health and safety compliance in facility management requires:",
        "options": ["Only senior management to be aware of safety regulations", "Ensuring all facilities, equipment and maintenance activities comply with relevant health, safety and environmental legislation", "Conducting safety audits only when an incident occurs", "Delegating all safety responsibilities to contractors"],
        "correct_answer": "Ensuring all facilities, equipment and maintenance activities comply with relevant health, safety and environmental legislation"
    },
    {
        "question": "Space management in facility management involves:",
        "options": ["Only managing car parking spaces", "Planning and optimising the use of physical space to meet organisational needs efficiently and cost-effectively", "Designing new office buildings", "Managing only storage areas"],
        "correct_answer": "Planning and optimising the use of physical space to meet organisational needs efficiently and cost-effectively"
    },
    {
        "question": "Energy management in facilities is important because:",
        "options": ["It only affects the company's marketing image", "Effective energy management reduces operational costs, minimises environmental impact and supports sustainability goals", "Energy costs are fixed and cannot be reduced", "It is only relevant for manufacturing facilities"],
        "correct_answer": "Effective energy management reduces operational costs, minimises environmental impact and supports sustainability goals"
    },
    {
        "question": "A Service Level Agreement (SLA) in facility management defines:",
        "options": ["The salary structure for facilities staff", "The agreed standards of service, response times and performance expectations between the facilities team and internal or external service providers", "The building's insurance coverage", "The annual maintenance budget"],
        "correct_answer": "The agreed standards of service, response times and performance expectations between the facilities team and internal or external service providers"
    },
    {
        "question": "Total Productive Maintenance (TPM) in facility management aims to:",
        "options": ["Eliminate all maintenance activities through automation", "Involve all employees in maintaining equipment and facilities to maximise productivity and minimise downtime", "Outsource all maintenance to specialist contractors", "Focus maintenance efforts only on critical equipment"],
        "correct_answer": "Involve all employees in maintaining equipment and facilities to maximise productivity and minimise downtime"
    },
    {
        "question": "Risk assessment in facility maintenance involves:",
        "options": ["Identifying only financial risks to the organisation", "Identifying potential hazards, assessing their likelihood and impact, and implementing controls to reduce risk to acceptable levels", "Conducting annual fire drills only", "Reviewing the maintenance budget for cost overruns"],
        "correct_answer": "Identifying potential hazards, assessing their likelihood and impact, and implementing controls to reduce risk to acceptable levels"
    },
    {
        "question": "Outsourcing facility management services means:",
        "options": ["The organisation retains full control of all maintenance activities", "Contracting external specialist providers to deliver some or all facility management services on behalf of the organisation", "Eliminating the internal facilities team entirely", "Only outsourcing cleaning and security services"],
        "correct_answer": "Contracting external specialist providers to deliver some or all facility management services on behalf of the organisation"
    },
    {
        "question": "Key Performance Indicators (KPIs) commonly used in facility management include:",
        "options": ["Employee turnover rate and marketing spend", "Maintenance response time, asset uptime, cost per square metre and energy consumption per unit", "Sales revenue and gross profit margin", "Customer acquisition cost and conversion rate"],
        "correct_answer": "Maintenance response time, asset uptime, cost per square metre and energy consumption per unit"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "facility management", "$options": "i"}})
    if not course:
        print("Course not found")
        return
    print(f"Found: {course['title']}")
    module = await db.modules.find_one({"course_id": course["id"]})
    existing = await db.quizzes.find_one({"module_id": module["id"]})
    if existing:
        await db.quizzes.delete_one({"module_id": module["id"]})
        print("Removed existing quiz")
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module["id"],
        "course_id": course["id"],
        "title": "Facility Management: Maintenance and Repairs - Final Assessment",
        "description": "Test your knowledge of facility management, preventive and corrective maintenance, asset management and compliance. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
