import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Supply chain risk management is defined as:",
        "options": ["Eliminating all risks from the supply chain", "The identification, assessment and mitigation of risks that could disrupt the flow of goods, information or finances across the supply chain", "Managing only financial risks in procurement", "Insuring all goods in transit"],
        "correct_answer": "The identification, assessment and mitigation of risks that could disrupt the flow of goods, information or finances across the supply chain"
    },
    {
        "question": "Which of the following is an example of a supply-side risk?",
        "options": ["A sudden drop in customer demand", "A key supplier experiencing a factory fire that halts production", "A competitor launching a new product", "A change in consumer preferences"],
        "correct_answer": "A key supplier experiencing a factory fire that halts production"
    },
    {
        "question": "A risk matrix in supply chain management is used to:",
        "options": ["Calculate the financial cost of all risks", "Prioritise risks by plotting their likelihood against their potential impact", "List all suppliers in order of importance", "Map the physical flow of goods through the supply chain"],
        "correct_answer": "Prioritise risks by plotting their likelihood against their potential impact"
    },
    {
        "question": "Single-source supply risk occurs when:",
        "options": ["A company uses too many suppliers", "A company relies on only one supplier for a critical component, creating vulnerability if that supplier fails", "A company sources from multiple countries", "A company has excess inventory"],
        "correct_answer": "A company relies on only one supplier for a critical component, creating vulnerability if that supplier fails"
    },
    {
        "question": "Supply chain disruption risk can be mitigated by:",
        "options": ["Reducing the number of suppliers to simplify management", "Diversifying the supplier base, holding safety stock and developing business continuity plans", "Eliminating all safety stock to reduce costs", "Outsourcing all supply chain decisions to a third party"],
        "correct_answer": "Diversifying the supplier base, holding safety stock and developing business continuity plans"
    },
    {
        "question": "Geopolitical risk in supply chain management refers to:",
        "options": ["Risks arising from poor warehouse management", "Disruptions caused by political instability, trade wars, sanctions or regulatory changes in supplier countries", "Financial risks from currency fluctuations only", "Risks from natural disasters only"],
        "correct_answer": "Disruptions caused by political instability, trade wars, sanctions or regulatory changes in supplier countries"
    },
    {
        "question": "A Business Continuity Plan (BCP) in supply chain risk management is designed to:",
        "options": ["Maximise profits during normal operations", "Ensure the organisation can continue critical supply chain operations during and after a major disruption", "Eliminate all supply chain risks permanently", "Reduce the number of suppliers"],
        "correct_answer": "Ensure the organisation can continue critical supply chain operations during and after a major disruption"
    },
    {
        "question": "Demand-side risk in supply chain management includes:",
        "options": ["Supplier insolvency", "Sudden changes in customer demand that create excess inventory or stockouts", "Port congestion and shipping delays", "Raw material price increases"],
        "correct_answer": "Sudden changes in customer demand that create excess inventory or stockouts"
    },
    {
        "question": "Supply chain risk visibility is important because:",
        "options": ["It allows companies to eliminate all suppliers", "Early identification of potential disruptions enables proactive mitigation before they escalate into major problems", "It reduces the need for safety stock", "It eliminates the need for supplier contracts"],
        "correct_answer": "Early identification of potential disruptions enables proactive mitigation before they escalate into major problems"
    },
    {
        "question": "Which of the following is a financial risk in supply chain management?",
        "options": ["A supplier's factory flooding", "Currency exchange rate fluctuations that increase the cost of imported goods", "A logistics provider going on strike", "A product recall due to quality issues"],
        "correct_answer": "Currency exchange rate fluctuations that increase the cost of imported goods"
    },
    {
        "question": "Risk transfer in supply chain management can be achieved through:",
        "options": ["Ignoring low-probability risks", "Insurance, contractual clauses and hedging strategies that shift financial exposure to another party", "Reducing the number of supply chain tiers", "Increasing inventory levels"],
        "correct_answer": "Insurance, contractual clauses and hedging strategies that shift financial exposure to another party"
    },
    {
        "question": "The four main strategies for managing supply chain risk are:",
        "options": ["Ignore, Monitor, Escalate, Close", "Avoid, Reduce, Transfer and Accept", "Plan, Do, Check, Act", "Identify, Assess, Respond, Review"],
        "correct_answer": "Avoid, Reduce, Transfer and Accept"
    },
    {
        "question": "Cybersecurity risk in modern supply chains refers to:",
        "options": ["Physical theft of goods from warehouses", "Threats to digital systems, data and connected supply chain technologies that could disrupt operations or compromise sensitive information", "Risks from counterfeit products only", "Employee fraud in procurement"],
        "correct_answer": "Threats to digital systems, data and connected supply chain technologies that could disrupt operations or compromise sensitive information"
    },
    {
        "question": "Supplier financial risk assessment involves:",
        "options": ["Reviewing only the supplier's product quality", "Evaluating a supplier's financial stability to assess the risk of insolvency or inability to fulfil orders", "Checking the supplier's marketing strategy", "Reviewing the supplier's employee headcount"],
        "correct_answer": "Evaluating a supplier's financial stability to assess the risk of insolvency or inability to fulfil orders"
    },
    {
        "question": "A proactive approach to supply chain risk management involves:",
        "options": ["Responding to disruptions only after they occur", "Continuously monitoring risk indicators, scenario planning and building resilience before disruptions happen", "Reducing all supply chain costs regardless of risk impact", "Eliminating all international suppliers"],
        "correct_answer": "Continuously monitoring risk indicators, scenario planning and building resilience before disruptions happen"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "understanding.*supply.*chain.*risk", "$options": "i"}})
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
        "title": "Supply Chain Risk Management - Final Assessment",
        "description": "Test your knowledge of supply chain risk identification, assessment, mitigation strategies and business continuity. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
