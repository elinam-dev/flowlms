import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "A freight broker's primary role is to:",
        "options": ["Own and operate trucks for cargo transport", "Act as an intermediary between shippers and carriers to arrange the transportation of goods", "Manage warehouse storage for importers", "Provide customs clearance services only"],
        "correct_answer": "Act as an intermediary between shippers and carriers to arrange the transportation of goods"
    },
    {
        "question": "In the freight brokerage industry, a 'shipper' refers to:",
        "options": ["The company that owns the trucks", "The entity that needs goods transported from one location to another", "The freight broker themselves", "The customs authority"],
        "correct_answer": "The entity that needs goods transported from one location to another"
    },
    {
        "question": "A freight broker is legally required to obtain which of the following before operating in the USA?",
        "options": ["A commercial driving licence", "A broker authority licence from the FMCSA and a surety bond", "A warehouse operating permit", "An import/export licence"],
        "correct_answer": "A broker authority licence from the FMCSA and a surety bond"
    },
    {
        "question": "The purpose of a surety bond in freight brokerage is to:",
        "options": ["Insure the cargo against damage", "Provide financial protection to shippers and carriers in case the broker fails to fulfil payment obligations", "Cover the broker's operating expenses", "Guarantee on-time delivery of all shipments"],
        "correct_answer": "Provide financial protection to shippers and carriers in case the broker fails to fulfil payment obligations"
    },
    {
        "question": "Which of the following best describes the freight brokerage industry's role in the supply chain?",
        "options": ["It replaces the need for logistics companies", "It connects shippers with carriers efficiently, improving capacity utilisation and reducing transportation costs", "It only handles international shipments", "It manages inventory for manufacturers"],
        "correct_answer": "It connects shippers with carriers efficiently, improving capacity utilisation and reducing transportation costs"
    },
    {
        "question": "A load board in freight brokerage is used to:",
        "options": ["Track warehouse inventory levels", "Post available freight loads and available truck capacity so brokers and carriers can match shipments", "Schedule driver rest periods", "Calculate freight insurance premiums"],
        "correct_answer": "Post available freight loads and available truck capacity so brokers and carriers can match shipments"
    },
    {
        "question": "Freight broker licensing requirements are regulated in the USA by:",
        "options": ["The Department of Homeland Security", "The Federal Motor Carrier Safety Administration (FMCSA)", "The Federal Aviation Administration (FAA)", "The US Customs and Border Protection (CBP)"],
        "correct_answer": "The Federal Motor Carrier Safety Administration (FMCSA)"
    },
    {
        "question": "A carrier in freight brokerage refers to:",
        "options": ["The company that ships goods internationally", "The transportation company or owner-operator that physically moves the freight", "The freight broker's client", "The insurance provider for cargo"],
        "correct_answer": "The transportation company or owner-operator that physically moves the freight"
    },
    {
        "question": "Which document confirms the terms of a freight shipment between a broker and carrier?",
        "options": ["A bill of lading", "A rate confirmation sheet", "A customs declaration form", "A warehouse receipt"],
        "correct_answer": "A rate confirmation sheet"
    },
    {
        "question": "The bill of lading (BOL) in freight serves as:",
        "options": ["A payment receipt for freight charges", "A legal document that serves as a receipt of goods, a contract of carriage and a document of title", "An insurance certificate for cargo", "A customs clearance document only"],
        "correct_answer": "A legal document that serves as a receipt of goods, a contract of carriage and a document of title"
    },
    {
        "question": "Freight brokers generate revenue primarily through:",
        "options": ["Charging carriers a monthly subscription fee", "Earning a margin between the rate charged to the shipper and the rate paid to the carrier", "Selling cargo insurance policies", "Charging warehousing fees"],
        "correct_answer": "Earning a margin between the rate charged to the shipper and the rate paid to the carrier"
    },
    {
        "question": "Which of the following is a key responsibility of a freight broker?",
        "options": ["Driving the freight to its destination", "Vetting carriers for safety compliance, negotiating rates and coordinating shipment logistics", "Storing goods in transit", "Clearing goods through customs on behalf of importers"],
        "correct_answer": "Vetting carriers for safety compliance, negotiating rates and coordinating shipment logistics"
    },
    {
        "question": "Supply chain and logistics knowledge is important for a freight broker because:",
        "options": ["It allows them to drive trucks when needed", "Understanding the broader supply chain helps brokers provide better solutions, anticipate client needs and add strategic value", "It is required by law for all brokers", "It enables brokers to manage warehouse operations"],
        "correct_answer": "Understanding the broader supply chain helps brokers provide better solutions, anticipate client needs and add strategic value"
    },
    {
        "question": "Financial bonding requirements for freight brokers exist to:",
        "options": ["Fund the broker's marketing activities", "Ensure brokers have financial accountability and protect shippers and carriers from non-payment", "Cover the cost of cargo damage claims", "Pay for broker licensing fees"],
        "correct_answer": "Ensure brokers have financial accountability and protect shippers and carriers from non-payment"
    },
    {
        "question": "Which of the following is a growing trend in the freight brokerage industry?",
        "options": ["Returning to paper-based booking systems", "Digital freight platforms and technology-driven matching of loads and carriers in real time", "Reducing the use of data and analytics", "Eliminating the broker role through direct shipper-carrier relationships only"],
        "correct_answer": "Digital freight platforms and technology-driven matching of loads and carriers in real time"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "freight.*broker.*training", "$options": "i"}})
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
        "title": "Freight Broker Training - Final Assessment",
        "description": "Test your knowledge of freight brokerage, licensing, carrier relations, documentation and industry operations. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
