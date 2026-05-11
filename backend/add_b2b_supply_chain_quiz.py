import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "B2B supply chain management differs from B2C supply chain management primarily because:",
        "options": ["B2B involves smaller order quantities", "B2B transactions involve businesses buying from other businesses, typically with larger volumes, longer relationships and more complex procurement processes", "B2B supply chains are always shorter", "B2B does not require logistics management"],
        "correct_answer": "B2B transactions involve businesses buying from other businesses, typically with larger volumes, longer relationships and more complex procurement processes"
    },
    {
        "question": "Procurement in B2B supply chain management involves:",
        "options": ["Only purchasing raw materials", "The end-to-end process of identifying needs, sourcing suppliers, negotiating contracts and managing supplier relationships", "Managing customer orders only", "Setting retail prices for products"],
        "correct_answer": "The end-to-end process of identifying needs, sourcing suppliers, negotiating contracts and managing supplier relationships"
    },
    {
        "question": "A Request for Proposal (RFP) in B2B procurement is used to:",
        "options": ["Request payment from customers", "Invite suppliers to submit detailed proposals for providing goods or services, enabling comparison and selection", "Propose a new product to the market", "Request a price reduction from an existing supplier"],
        "correct_answer": "Invite suppliers to submit detailed proposals for providing goods or services, enabling comparison and selection"
    },
    {
        "question": "Vendor qualification in B2B supply chain management ensures that:",
        "options": ["All suppliers charge the same price", "Suppliers meet defined quality, financial, compliance and capability standards before being approved", "Only local suppliers are used", "Suppliers are paid in advance"],
        "correct_answer": "Suppliers meet defined quality, financial, compliance and capability standards before being approved"
    },
    {
        "question": "A Service Level Agreement (SLA) in B2B supply chain management defines:",
        "options": ["The salary structure for supply chain staff", "The agreed performance standards, delivery timelines and quality expectations between a buyer and supplier", "The insurance coverage for goods in transit", "The payment terms for all transactions"],
        "correct_answer": "The agreed performance standards, delivery timelines and quality expectations between a buyer and supplier"
    },
    {
        "question": "Inventory optimisation in B2B supply chains aims to:",
        "options": ["Maximise stock levels to prevent any stockouts", "Balance holding costs against service levels by maintaining the right quantity of stock at the right time", "Eliminate all safety stock", "Order inventory only when stock reaches zero"],
        "correct_answer": "Balance holding costs against service levels by maintaining the right quantity of stock at the right time"
    },
    {
        "question": "The Kraljic Matrix is used in B2B supply chain management to:",
        "options": ["Map warehouse storage locations", "Categorise purchased items by supply risk and profit impact to develop appropriate sourcing strategies", "Calculate the total cost of ownership", "Evaluate supplier financial stability"],
        "correct_answer": "Categorise purchased items by supply risk and profit impact to develop appropriate sourcing strategies"
    },
    {
        "question": "Supply chain integration in B2B refers to:",
        "options": ["Merging all suppliers into one company", "Aligning processes, systems and information flows between buyers and suppliers to improve efficiency and responsiveness", "Integrating all products into a single catalogue", "Combining logistics and warehousing under one provider"],
        "correct_answer": "Aligning processes, systems and information flows between buyers and suppliers to improve efficiency and responsiveness"
    },
    {
        "question": "Which of the following is a key risk in B2B supply chain management?",
        "options": ["Having too many customers", "Single-source dependency, where reliance on one supplier creates vulnerability to disruption", "Offering too many product variants", "Having a large number of approved suppliers"],
        "correct_answer": "Single-source dependency, where reliance on one supplier creates vulnerability to disruption"
    },
    {
        "question": "Demand-driven supply chain management in B2B means:",
        "options": ["Producing goods based on forecasts only", "Aligning supply chain activities with actual customer demand signals to reduce waste and improve responsiveness", "Maximising production output regardless of orders", "Setting supply based on historical averages only"],
        "correct_answer": "Aligning supply chain activities with actual customer demand signals to reduce waste and improve responsiveness"
    },
    {
        "question": "Total Cost of Ownership (TCO) analysis in B2B procurement considers:",
        "options": ["Only the unit purchase price", "All costs including acquisition, transportation, quality, maintenance, risk and disposal over the product's lifetime", "Only the supplier's quoted price and delivery cost", "The cost of the buyer's internal procurement team only"],
        "correct_answer": "All costs including acquisition, transportation, quality, maintenance, risk and disposal over the product's lifetime"
    },
    {
        "question": "Collaborative planning in B2B supply chains involves:",
        "options": ["Each company planning independently without sharing information", "Buyers and suppliers jointly sharing forecasts, inventory data and production plans to synchronise supply and demand", "The buyer dictating all planning decisions to suppliers", "Planning only for peak demand periods"],
        "correct_answer": "Buyers and suppliers jointly sharing forecasts, inventory data and production plans to synchronise supply and demand"
    },
    {
        "question": "Which document is typically used to formalise a B2B purchase transaction?",
        "options": ["A marketing brochure", "A Purchase Order (PO) that specifies the goods, quantities, agreed price and delivery terms", "An employee contract", "A bank statement"],
        "correct_answer": "A Purchase Order (PO) that specifies the goods, quantities, agreed price and delivery terms"
    },
    {
        "question": "Supplier performance management in B2B supply chains involves:",
        "options": ["Only monitoring delivery times", "Regularly measuring, reviewing and improving supplier performance against agreed KPIs including quality, delivery, cost and service", "Replacing underperforming suppliers immediately without review", "Conducting annual audits only"],
        "correct_answer": "Regularly measuring, reviewing and improving supplier performance against agreed KPIs including quality, delivery, cost and service"
    },
    {
        "question": "Digital transformation in B2B supply chain management enables:",
        "options": ["Elimination of all human roles in the supply chain", "Real-time data sharing, automated procurement, predictive analytics and improved end-to-end visibility across the supply network", "Reduction of all supplier relationships to one platform", "Replacement of all physical goods with digital products"],
        "correct_answer": "Real-time data sharing, automated procurement, predictive analytics and improved end-to-end visibility across the supply network"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "b2b.*supply.*chain.*management", "$options": "i"}})
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
        "title": "B2B Supply Chain Management - Final Assessment",
        "description": "Test your knowledge of B2B procurement, supplier management, inventory optimisation and supply chain integration. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
