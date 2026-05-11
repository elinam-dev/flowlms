import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Supply chain management (SCM) is defined as:",
        "options": ["Managing only the transportation of goods", "The coordination and management of all activities involved in sourcing, procurement, production and delivery of products to the end customer", "Managing customer relationships only", "The financial management of procurement budgets"],
        "correct_answer": "The coordination and management of all activities involved in sourcing, procurement, production and delivery of products to the end customer"
    },
    {
        "question": "The five key components of supply chain management are:",
        "options": ["Plan, Source, Make, Deliver, Return", "Buy, Store, Move, Sell, Invoice", "Forecast, Order, Produce, Ship, Pay", "Design, Build, Test, Deploy, Review"],
        "correct_answer": "Plan, Source, Make, Deliver, Return"
    },
    {
        "question": "Supply chain network design involves:",
        "options": ["Designing the company's IT infrastructure", "Determining the optimal number, location and capacity of facilities such as factories, warehouses and distribution centres", "Designing product packaging", "Planning the company's marketing network"],
        "correct_answer": "Determining the optimal number, location and capacity of facilities such as factories, warehouses and distribution centres"
    },
    {
        "question": "The SCOR (Supply Chain Operations Reference) model provides:",
        "options": ["A financial reporting framework for supply chains", "A standardised framework for evaluating and improving supply chain performance across Plan, Source, Make, Deliver and Return processes", "A legal framework for supplier contracts", "A model for calculating supply chain costs only"],
        "correct_answer": "A standardised framework for evaluating and improving supply chain performance across Plan, Source, Make, Deliver and Return processes"
    },
    {
        "question": "Demand planning in supply chain management involves:",
        "options": ["Planning only for peak season demand", "Forecasting future customer demand to align supply chain resources, inventory and production capacity accordingly", "Setting sales targets for the marketing team", "Planning the company's capital expenditure budget"],
        "correct_answer": "Forecasting future customer demand to align supply chain resources, inventory and production capacity accordingly"
    },
    {
        "question": "The bullwhip effect in supply chain management describes:",
        "options": ["The physical cracking of a whip used in warehouse operations", "The amplification of demand variability as orders move upstream through the supply chain, causing inefficiency and excess inventory", "A lean technique for reducing lead times", "The impact of weather disruptions on logistics"],
        "correct_answer": "The amplification of demand variability as orders move upstream through the supply chain, causing inefficiency and excess inventory"
    },
    {
        "question": "Sustainable supply chain management involves:",
        "options": ["Focusing only on cost reduction", "Integrating environmental, social and governance (ESG) practices into supply chain decisions to minimise negative impacts", "Eliminating all international suppliers", "Maximising production output regardless of environmental impact"],
        "correct_answer": "Integrating environmental, social and governance (ESG) practices into supply chain decisions to minimise negative impacts"
    },
    {
        "question": "Third-Party Logistics (3PL) providers offer:",
        "options": ["Only warehousing services", "Outsourced logistics services including transportation, warehousing, distribution and value-added services", "Only customs clearance services", "Financial services for supply chain transactions"],
        "correct_answer": "Outsourced logistics services including transportation, warehousing, distribution and value-added services"
    },
    {
        "question": "Agile supply chain management is characterised by:",
        "options": ["Rigid, standardised processes with no flexibility", "The ability to respond quickly and flexibly to changes in demand, supply disruptions or market conditions", "Maximising efficiency at the expense of responsiveness", "Focusing only on cost minimisation"],
        "correct_answer": "The ability to respond quickly and flexibly to changes in demand, supply disruptions or market conditions"
    },
    {
        "question": "Inventory turnover ratio measures:",
        "options": ["The number of times inventory is ordered per year", "How many times inventory is sold and replaced over a given period — a higher ratio indicates efficient inventory management", "The total value of inventory held at year end", "The percentage of inventory that is damaged or obsolete"],
        "correct_answer": "How many times inventory is sold and replaced over a given period — a higher ratio indicates efficient inventory management"
    },
    {
        "question": "Global sourcing in supply chain management refers to:",
        "options": ["Buying all goods from domestic suppliers only", "Procuring goods and services from international suppliers to leverage cost advantages, quality or capabilities not available locally", "Sourcing only from a single global supplier", "Importing finished goods for resale only"],
        "correct_answer": "Procuring goods and services from international suppliers to leverage cost advantages, quality or capabilities not available locally"
    },
    {
        "question": "The concept of 'lean supply chain' focuses on:",
        "options": ["Maximising inventory at every stage of the supply chain", "Eliminating waste, reducing lead times and improving flow throughout the supply chain to deliver value to the customer", "Reducing the number of supply chain partners", "Outsourcing all supply chain activities"],
        "correct_answer": "Eliminating waste, reducing lead times and improving flow throughout the supply chain to deliver value to the customer"
    },
    {
        "question": "Supply chain analytics is used to:",
        "options": ["Replace all human decision-making in the supply chain", "Analyse supply chain data to gain insights, improve forecasting, identify inefficiencies and support strategic decisions", "Manage supplier payment terms only", "Track employee performance in the warehouse"],
        "correct_answer": "Analyse supply chain data to gain insights, improve forecasting, identify inefficiencies and support strategic decisions"
    },
    {
        "question": "Reverse logistics in supply chain management involves:",
        "options": ["Moving goods from the factory to the customer", "Managing the return flow of goods from customers back through the supply chain for reuse, repair, recycling or disposal", "Reversing incorrect purchase orders", "Moving goods between distribution centres"],
        "correct_answer": "Managing the return flow of goods from customers back through the supply chain for reuse, repair, recycling or disposal"
    },
    {
        "question": "A key strategic objective of supply chain management is to:",
        "options": ["Maximise inventory levels to prevent stockouts at all costs", "Deliver the right product, in the right quantity, to the right place, at the right time and at the right cost", "Minimise the number of suppliers regardless of risk", "Focus exclusively on reducing transportation costs"],
        "correct_answer": "Deliver the right product, in the right quantity, to the right place, at the right time and at the right cost"
    },
    {
        "question": "Digital supply chain transformation enables organisations to:",
        "options": ["Eliminate all physical supply chain activities", "Leverage technologies such as IoT, AI, blockchain and cloud platforms to improve visibility, efficiency and resilience across the supply chain", "Reduce the need for supply chain professionals", "Replace all suppliers with automated systems"],
        "correct_answer": "Leverage technologies such as IoT, AI, blockchain and cloud platforms to improve visibility, efficiency and resilience across the supply chain"
    },
    {
        "question": "Collaborative supply chain relationships are built on:",
        "options": ["Adversarial negotiations to achieve the lowest price", "Trust, transparency, shared goals and mutual benefit between supply chain partners", "Keeping all supply chain data confidential from partners", "Maximising the buyer's power over suppliers"],
        "correct_answer": "Trust, transparency, shared goals and mutual benefit between supply chain partners"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "diploma.*supply.*chain.*management", "$options": "i"}})
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
        "title": "Diploma in Supply Chain Management - Final Assessment",
        "description": "Test your knowledge of supply chain strategy, planning, logistics, risk, sustainability and digital transformation. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
