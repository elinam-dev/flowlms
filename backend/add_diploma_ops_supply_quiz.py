import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Operations management is primarily concerned with:",
        "options": ["Managing financial investments", "Designing, controlling and improving the processes that produce and deliver goods and services", "Developing marketing campaigns", "Managing employee recruitment"],
        "correct_answer": "Designing, controlling and improving the processes that produce and deliver goods and services"
    },
    {
        "question": "Supply management involves:",
        "options": ["Only managing warehouse inventory", "Strategically sourcing, procuring and managing suppliers to ensure the right goods and services are available at the right time, cost and quality", "Managing customer relationships only", "Setting product prices"],
        "correct_answer": "Strategically sourcing, procuring and managing suppliers to ensure the right goods and services are available at the right time, cost and quality"
    },
    {
        "question": "Just-In-Time (JIT) inventory management aims to:",
        "options": ["Maintain large safety stock buffers", "Receive goods only when needed in the production process, minimising inventory holding costs", "Order inventory once per year in bulk", "Eliminate all supplier relationships"],
        "correct_answer": "Receive goods only when needed in the production process, minimising inventory holding costs"
    },
    {
        "question": "The Economic Order Quantity (EOQ) model determines:",
        "options": ["The maximum inventory level a warehouse can hold", "The optimal order quantity that minimises total inventory ordering and holding costs", "The reorder point for safety stock", "The number of suppliers needed for each product"],
        "correct_answer": "The optimal order quantity that minimises total inventory ordering and holding costs"
    },
    {
        "question": "Capacity planning in operations management involves:",
        "options": ["Hiring the maximum number of employees possible", "Determining the production capacity needed to meet current and future demand", "Reducing all operational costs by 20%", "Planning only for peak season demand"],
        "correct_answer": "Determining the production capacity needed to meet current and future demand"
    },
    {
        "question": "A key performance indicator (KPI) commonly used in supply management is:",
        "options": ["Employee satisfaction score", "On-Time In-Full (OTIF) delivery rate", "Marketing conversion rate", "Net Promoter Score (NPS)"],
        "correct_answer": "On-Time In-Full (OTIF) delivery rate"
    },
    {
        "question": "Strategic sourcing differs from traditional purchasing in that it:",
        "options": ["Focuses only on getting the lowest price", "Takes a long-term, relationship-based approach to supplier selection that considers total cost of ownership and strategic fit", "Avoids long-term supplier contracts", "Is only used for capital expenditure"],
        "correct_answer": "Takes a long-term, relationship-based approach to supplier selection that considers total cost of ownership and strategic fit"
    },
    {
        "question": "Total Cost of Ownership (TCO) in procurement includes:",
        "options": ["Only the purchase price of goods", "All costs associated with acquiring, using, maintaining and disposing of a product over its lifetime", "Only transportation and logistics costs", "The supplier's profit margin"],
        "correct_answer": "All costs associated with acquiring, using, maintaining and disposing of a product over its lifetime"
    },
    {
        "question": "Demand forecasting in operations management is used to:",
        "options": ["Set employee performance targets", "Predict future customer demand to plan production, inventory and resource requirements", "Determine the company's marketing budget", "Calculate the company's tax liability"],
        "correct_answer": "Predict future customer demand to plan production, inventory and resource requirements"
    },
    {
        "question": "A make-or-buy decision in operations management involves:",
        "options": ["Deciding whether to manufacture a product in-house or outsource it to a supplier", "Choosing between two marketing strategies", "Deciding whether to buy or lease office space", "Selecting between two distribution channels"],
        "correct_answer": "Deciding whether to manufacture a product in-house or outsource it to a supplier"
    },
    {
        "question": "Supplier relationship management (SRM) aims to:",
        "options": ["Reduce the number of suppliers to one", "Develop and manage strategic partnerships with key suppliers to drive mutual value and performance improvement", "Negotiate the lowest possible price from all suppliers", "Eliminate all long-term supplier contracts"],
        "correct_answer": "Develop and manage strategic partnerships with key suppliers to drive mutual value and performance improvement"
    },
    {
        "question": "Process mapping in operations management is used to:",
        "options": ["Track employee attendance", "Visually document the steps, inputs and outputs of a process to identify inefficiencies and improvement opportunities", "Map the company's organisational hierarchy", "Plan the company's annual budget"],
        "correct_answer": "Visually document the steps, inputs and outputs of a process to identify inefficiencies and improvement opportunities"
    },
    {
        "question": "Quality management in operations focuses on:",
        "options": ["Reducing production speed to improve accuracy", "Ensuring products and services consistently meet or exceed customer requirements and specifications", "Increasing the number of quality inspectors", "Reducing the cost of raw materials only"],
        "correct_answer": "Ensuring products and services consistently meet or exceed customer requirements and specifications"
    },
    {
        "question": "Logistics management encompasses:",
        "options": ["Only warehouse management", "The planning, implementation and control of the efficient flow and storage of goods, services and information from origin to destination", "Only transportation of finished goods", "Managing customer returns only"],
        "correct_answer": "The planning, implementation and control of the efficient flow and storage of goods, services and information from origin to destination"
    },
    {
        "question": "Continuous improvement in operations management is best supported by:",
        "options": ["Large, infrequent transformation projects only", "A culture of regular, incremental improvements driven by data, employee involvement and structured problem-solving", "Reducing employee autonomy", "Outsourcing all improvement activities to consultants"],
        "correct_answer": "A culture of regular, incremental improvements driven by data, employee involvement and structured problem-solving"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "diploma.*operations.*supply", "$options": "i"}})
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
        "title": "Diploma in Operations and Supply Management - Final Assessment",
        "description": "Test your knowledge of operations management, procurement, inventory, logistics and supply strategy. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
