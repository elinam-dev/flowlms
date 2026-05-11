import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Sea export forwarding refers to:",
        "options": ["Managing domestic road freight only", "The process of organising and managing the shipment of goods from an exporter to an overseas buyer via sea transport", "Importing goods from overseas suppliers", "Managing air freight shipments exclusively"],
        "correct_answer": "The process of organising and managing the shipment of goods from an exporter to an overseas buyer via sea transport"
    },
    {
        "question": "A freight forwarder in sea export acts as:",
        "options": ["The owner of the shipping vessel", "An intermediary that arranges transportation, documentation and customs clearance on behalf of the exporter", "The customs authority at the port", "The insurance underwriter for cargo"],
        "correct_answer": "An intermediary that arranges transportation, documentation and customs clearance on behalf of the exporter"
    },
    {
        "question": "The Bill of Lading (B/L) in sea export serves as:",
        "options": ["A customs duty payment receipt", "A document of title, receipt of goods and contract of carriage between the shipper and the shipping line", "An insurance certificate for the cargo", "A packing list for the shipment"],
        "correct_answer": "A document of title, receipt of goods and contract of carriage between the shipper and the shipping line"
    },
    {
        "question": "A pre-shipment inspection is conducted to:",
        "options": ["Inspect the shipping vessel before departure", "Verify that goods meet the required quality, quantity and specification standards before they are loaded for export", "Check the exporter's financial records", "Inspect the destination port facilities"],
        "correct_answer": "Verify that goods meet the required quality, quantity and specification standards before they are loaded for export"
    },
    {
        "question": "Export customs clearance involves:",
        "options": ["Paying import duties at the destination country", "Submitting the required export declarations and documentation to the customs authority to obtain permission to export goods", "Arranging marine insurance for the cargo", "Booking space on the shipping vessel"],
        "correct_answer": "Submitting the required export declarations and documentation to the customs authority to obtain permission to export goods"
    },
    {
        "question": "An FCL (Full Container Load) shipment means:",
        "options": ["The cargo fills only part of a container shared with other shippers", "The exporter's cargo fills an entire container exclusively", "The container is loaded at the port only", "The freight forwarder owns the container"],
        "correct_answer": "The exporter's cargo fills an entire container exclusively"
    },
    {
        "question": "An LCL (Less than Container Load) shipment is used when:",
        "options": ["The exporter has enough cargo to fill a full container", "The exporter's cargo is consolidated with other shippers' goods into a shared container", "The goods are too large for a standard container", "The shipment is sent by air freight"],
        "correct_answer": "The exporter's cargo is consolidated with other shippers' goods into a shared container"
    },
    {
        "question": "The shipping booking and confirmation process involves:",
        "options": ["Paying import duties in advance", "Reserving space on a vessel with the shipping line and receiving a booking confirmation with vessel and voyage details", "Completing the import customs declaration", "Arranging inland transportation at the destination"],
        "correct_answer": "Reserving space on a vessel with the shipping line and receiving a booking confirmation with vessel and voyage details"
    },
    {
        "question": "Packaging and labelling requirements in sea export are important because:",
        "options": ["They are optional for most shipments", "Proper packaging protects goods during transit and correct labelling ensures compliance with customs, safety and destination country regulations", "They only apply to hazardous goods", "They are only required for FCL shipments"],
        "correct_answer": "Proper packaging protects goods during transit and correct labelling ensures compliance with customs, safety and destination country regulations"
    },
    {
        "question": "Order management in sea export forwarding involves:",
        "options": ["Managing customer complaints after delivery", "Coordinating the end-to-end process from order receipt through production, documentation, booking and shipment to ensure timely delivery", "Only tracking the vessel's position at sea", "Managing the importer's warehouse operations"],
        "correct_answer": "Coordinating the end-to-end process from order receipt through production, documentation, booking and shipment to ensure timely delivery"
    },
    {
        "question": "Which document is used to declare the contents, value and origin of goods for export customs purposes?",
        "options": ["Bill of Lading", "Export Declaration (Customs Entry)", "Certificate of Origin", "Packing List"],
        "correct_answer": "Export Declaration (Customs Entry)"
    },
    {
        "question": "A Certificate of Origin in sea export is required to:",
        "options": ["Prove the exporter's identity", "Certify the country in which the goods were manufactured, which may affect import duties and trade agreement eligibility at the destination", "Confirm the vessel's registration", "Declare the value of the cargo for insurance purposes"],
        "correct_answer": "Certify the country in which the goods were manufactured, which may affect import duties and trade agreement eligibility at the destination"
    },
    {
        "question": "Marine cargo insurance in sea export is taken out to:",
        "options": ["Cover the shipping line against vessel damage", "Protect the cargo owner against financial loss if goods are damaged, lost or stolen during transit", "Cover the freight forwarder's liability", "Insure the exporter against non-payment by the buyer"],
        "correct_answer": "Protect the cargo owner against financial loss if goods are damaged, lost or stolen during transit"
    },
    {
        "question": "Key players in sea export forwarding include:",
        "options": ["Only the exporter and the shipping line", "The exporter, freight forwarder, shipping line, customs authority, port operator and the importer", "Only the freight forwarder and customs authority", "The exporter and the end consumer only"],
        "correct_answer": "The exporter, freight forwarder, shipping line, customs authority, port operator and the importer"
    },
    {
        "question": "Product sourcing and selection in the context of sea export involves:",
        "options": ["Selecting the shipping route only", "Identifying and qualifying suppliers who can produce goods to the required specification, quality and volume for export", "Choosing the destination market for the goods", "Selecting the type of container for the shipment"],
        "correct_answer": "Identifying and qualifying suppliers who can produce goods to the required specification, quality and volume for export"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "complete.*guide.*sea.*export", "$options": "i"}})
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
        "title": "The Complete Guide to Sea Export Forwarding - Final Assessment",
        "description": "Test your knowledge of sea export processes, documentation, customs clearance and key players in freight forwarding. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
