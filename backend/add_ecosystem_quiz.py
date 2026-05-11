import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "A supply chain ecosystem refers to:",
        "options": ["Only the relationship between a company and its direct suppliers", "The interconnected network of organisations, people, technology and resources involved in creating and delivering a product or service to the end customer", "The environmental impact of supply chain operations", "A company's internal production processes only"],
        "correct_answer": "The interconnected network of organisations, people, technology and resources involved in creating and delivering a product or service to the end customer"
    },
    {
        "question": "The key participants in a supply chain ecosystem typically include:",
        "options": ["Only manufacturers and retailers", "Suppliers, manufacturers, distributors, logistics providers, retailers and end customers", "Only the buying company and its direct suppliers", "Government regulators and financial institutions only"],
        "correct_answer": "Suppliers, manufacturers, distributors, logistics providers, retailers and end customers"
    },
    {
        "question": "Supply chain visibility refers to:",
        "options": ["The ability to see inside a warehouse", "The ability to track and monitor the movement of goods, information and finances across the entire supply chain in real time", "Publishing supply chain data publicly", "Monitoring only the final delivery to the customer"],
        "correct_answer": "The ability to track and monitor the movement of goods, information and finances across the entire supply chain in real time"
    },
    {
        "question": "Six Sigma is applied in supply chain management primarily to:",
        "options": ["Increase inventory levels", "Reduce defects, errors and variation in supply chain processes to improve quality and reliability", "Speed up all supply chain processes regardless of quality", "Eliminate all supplier relationships"],
        "correct_answer": "Reduce defects, errors and variation in supply chain processes to improve quality and reliability"
    },
    {
        "question": "The DMAIC framework applied to supply chain improvement stands for:",
        "options": ["Deliver, Manage, Analyse, Improve, Control", "Define, Measure, Analyse, Improve, Control", "Design, Monitor, Assess, Implement, Close", "Detect, Mitigate, Audit, Inspect, Correct"],
        "correct_answer": "Define, Measure, Analyse, Improve, Control"
    },
    {
        "question": "Which of the following is an example of applying Six Sigma in a supply chain context?",
        "options": ["Increasing the number of suppliers", "Reducing order fulfilment errors from 5% to below 0.1% through root cause analysis and process improvement", "Expanding warehouse capacity", "Outsourcing all logistics operations"],
        "correct_answer": "Reducing order fulfilment errors from 5% to below 0.1% through root cause analysis and process improvement"
    },
    {
        "question": "The bullwhip effect in a supply chain ecosystem describes:",
        "options": ["The physical movement of goods through the supply chain", "The amplification of demand variability as orders move upstream from retailer to manufacturer, causing inefficiency", "A lean technique for reducing waste", "The impact of weather on logistics operations"],
        "correct_answer": "The amplification of demand variability as orders move upstream from retailer to manufacturer, causing inefficiency"
    },
    {
        "question": "Collaboration in a supply chain ecosystem is important because:",
        "options": ["It eliminates the need for contracts between parties", "Sharing information and aligning goals across supply chain partners reduces waste, improves responsiveness and creates mutual value", "It allows one company to control all supply chain decisions", "It reduces the number of suppliers needed"],
        "correct_answer": "Sharing information and aligning goals across supply chain partners reduces waste, improves responsiveness and creates mutual value"
    },
    {
        "question": "A key metric used to measure supply chain ecosystem performance is:",
        "options": ["Employee turnover rate", "Perfect Order Rate — the percentage of orders delivered on time, in full, without damage and with correct documentation", "Marketing spend as a percentage of revenue", "Number of warehouse locations"],
        "correct_answer": "Perfect Order Rate — the percentage of orders delivered on time, in full, without damage and with correct documentation"
    },
    {
        "question": "Technology plays a role in supply chain ecosystems by:",
        "options": ["Replacing all human decision-making", "Enabling real-time data sharing, demand forecasting, inventory optimisation and end-to-end visibility across supply chain partners", "Reducing the need for supplier relationships", "Only automating warehouse picking operations"],
        "correct_answer": "Enabling real-time data sharing, demand forecasting, inventory optimisation and end-to-end visibility across supply chain partners"
    },
    {
        "question": "Lean principles applied to the supply chain ecosystem focus on:",
        "options": ["Maximising inventory at every stage", "Eliminating non-value-adding activities and waste across the entire supply chain to improve flow and reduce cost", "Increasing the number of supply chain tiers", "Standardising all products to reduce variety"],
        "correct_answer": "Eliminating non-value-adding activities and waste across the entire supply chain to improve flow and reduce cost"
    },
    {
        "question": "Supply chain resilience in an ecosystem context means:",
        "options": ["Having the lowest possible cost structure", "The ability to anticipate, adapt to and recover from disruptions while maintaining continuity of supply", "Eliminating all single-source suppliers immediately", "Holding maximum safety stock at all times"],
        "correct_answer": "The ability to anticipate, adapt to and recover from disruptions while maintaining continuity of supply"
    },
    {
        "question": "Which of the following best describes a Tier 1 supplier in a supply chain ecosystem?",
        "options": ["A supplier that provides raw materials to Tier 2 suppliers", "A supplier that directly supplies goods or services to the focal company", "The company's largest customer", "A logistics provider that manages final delivery"],
        "correct_answer": "A supplier that directly supplies goods or services to the focal company"
    },
    {
        "question": "Sustainability in a supply chain ecosystem involves:",
        "options": ["Focusing only on cost reduction", "Integrating environmental, social and governance (ESG) considerations into supply chain decisions to reduce impact and meet stakeholder expectations", "Eliminating all international suppliers", "Maximising production output regardless of environmental impact"],
        "correct_answer": "Integrating environmental, social and governance (ESG) considerations into supply chain decisions to reduce impact and meet stakeholder expectations"
    },
    {
        "question": "The integration of Six Sigma and supply chain ecosystem management delivers value by:",
        "options": ["Focusing only on internal process improvements", "Combining data-driven quality improvement with end-to-end supply chain optimisation to reduce defects, waste and variability across the network", "Replacing supply chain partners with automated systems", "Eliminating the need for performance measurement"],
        "correct_answer": "Combining data-driven quality improvement with end-to-end supply chain optimisation to reduce defects, waste and variability across the network"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "understanding.*supply.*chain.*ecosystem", "$options": "i"}})
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
        "title": "Supply Chain Ecosystem and Six Sigma - Final Assessment",
        "description": "Test your knowledge of supply chain ecosystems, Six Sigma application, DMAIC and supply chain performance. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
