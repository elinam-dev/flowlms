import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Incoterms are published by:",
        "options": ["The World Trade Organization (WTO)", "The International Chamber of Commerce (ICC)", "The United Nations (UN)", "The World Customs Organization (WCO)"],
        "correct_answer": "The International Chamber of Commerce (ICC)"
    },
    {
        "question": "The primary purpose of Incoterms is to:",
        "options": ["Set international tax rates on traded goods", "Define the responsibilities of buyers and sellers for the delivery of goods, including risk transfer and cost allocation", "Regulate import and export documentation", "Determine the currency used in international trade"],
        "correct_answer": "Define the responsibilities of buyers and sellers for the delivery of goods, including risk transfer and cost allocation"
    },
    {
        "question": "Under EXW (Ex Works), the seller's obligation is to:",
        "options": ["Deliver goods to the buyer's premises", "Make goods available at the seller's premises — the buyer bears all costs and risks from that point", "Pay for all freight and insurance", "Clear goods through export customs"],
        "correct_answer": "Make goods available at the seller's premises — the buyer bears all costs and risks from that point"
    },
    {
        "question": "Under DDP (Delivered Duty Paid), who bears the maximum responsibility?",
        "options": ["The buyer", "The freight forwarder", "The seller", "The shipping line"],
        "correct_answer": "The seller"
    },
    {
        "question": "FOB (Free On Board) means the seller's risk transfers to the buyer when:",
        "options": ["The goods arrive at the buyer's warehouse", "The goods are loaded on board the vessel at the named port of shipment", "The seller hands goods to the freight forwarder", "The goods clear import customs"],
        "correct_answer": "The goods are loaded on board the vessel at the named port of shipment"
    },
    {
        "question": "CIF (Cost, Insurance and Freight) requires the seller to pay for:",
        "options": ["Only the cost of goods", "The cost of goods, marine insurance and freight to the named destination port", "All costs including import duties", "Only freight charges to the destination"],
        "correct_answer": "The cost of goods, marine insurance and freight to the named destination port"
    },
    {
        "question": "Which Incoterm is suitable for all modes of transport including multimodal?",
        "options": ["FOB", "CFR", "CIF", "DAP (Delivered at Place)"],
        "correct_answer": "DAP (Delivered at Place)"
    },
    {
        "question": "FCA (Free Carrier) transfers risk from seller to buyer when:",
        "options": ["Goods arrive at the destination port", "The seller delivers goods to the named carrier or another nominated party at the agreed place", "Goods are loaded onto the vessel", "Import customs clearance is completed"],
        "correct_answer": "The seller delivers goods to the named carrier or another nominated party at the agreed place"
    },
    {
        "question": "Which Incoterm places the least obligation on the buyer?",
        "options": ["EXW", "FOB", "DDP", "FCA"],
        "correct_answer": "DDP"
    },
    {
        "question": "CPT (Carriage Paid To) means:",
        "options": ["The buyer pays all freight costs", "The seller pays freight to the named destination but risk transfers to the buyer when goods are handed to the first carrier", "The seller is responsible for all costs and risks to the destination", "Insurance is included in the seller's obligations"],
        "correct_answer": "The seller pays freight to the named destination but risk transfers to the buyer when goods are handed to the first carrier"
    },
    {
        "question": "Incoterms 2020 introduced a change to FCA that allows:",
        "options": ["The buyer to arrange insurance on behalf of the seller", "The buyer to instruct their bank to issue a bill of lading with an on-board notation when FCA is used with letters of credit", "The seller to clear import customs under FCA", "FCA to be used only for sea freight"],
        "correct_answer": "The buyer to instruct their bank to issue a bill of lading with an on-board notation when FCA is used with letters of credit"
    },
    {
        "question": "Which group of Incoterms (E, F, C, D) places the most responsibility on the seller?",
        "options": ["E terms", "F terms", "C terms", "D terms"],
        "correct_answer": "D terms"
    },
    {
        "question": "Under CFR (Cost and Freight), who is responsible for arranging marine insurance?",
        "options": ["The seller must arrange insurance", "Neither party is obligated — the buyer should arrange their own insurance", "The freight forwarder arranges insurance", "The shipping line provides automatic insurance"],
        "correct_answer": "Neither party is obligated — the buyer should arrange their own insurance"
    },
    {
        "question": "Incoterms define which of the following?",
        "options": ["The price of goods and payment terms", "Transfer of risk, allocation of costs and delivery obligations between buyer and seller", "Import and export tax rates", "The governing law of the sales contract"],
        "correct_answer": "Transfer of risk, allocation of costs and delivery obligations between buyer and seller"
    },
    {
        "question": "DAP (Delivered at Place) requires the seller to:",
        "options": ["Clear goods through import customs and pay import duties", "Deliver goods to the named place ready for unloading, with the buyer responsible for import clearance and duties", "Hand goods to the carrier at the port of origin", "Pay all costs including unloading at destination"],
        "correct_answer": "Deliver goods to the named place ready for unloading, with the buyer responsible for import clearance and duties"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "incoterms", "$options": "i"}})
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
        "title": "Introduction to Commercial Terms (Incoterms) - Final Assessment",
        "description": "Test your knowledge of Incoterms 2020, risk transfer, cost allocation and seller/buyer obligations. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
