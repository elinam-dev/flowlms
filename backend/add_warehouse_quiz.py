import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "The primary function of a warehouse in a supply chain is to:",
        "options": ["Generate revenue through retail sales", "Store goods and facilitate the efficient movement of products between suppliers and customers", "Manufacture finished goods", "Manage supplier contracts"],
        "correct_answer": "Store goods and facilitate the efficient movement of products between suppliers and customers"
    },
    {
        "question": "Which of the following is a key principle of effective warehouse management?",
        "options": ["Maximising inventory levels at all times", "Optimising space utilisation, minimising handling and ensuring accurate stock records", "Reducing the number of warehouse staff", "Storing all products in the same location"],
        "correct_answer": "Optimising space utilisation, minimising handling and ensuring accurate stock records"
    },
    {
        "question": "FIFO (First In, First Out) is a warehouse principle that ensures:",
        "options": ["The most recently received stock is picked first", "The oldest stock is picked and dispatched first, reducing the risk of expiry or obsolescence", "Stock is rotated randomly", "High-value items are always picked first"],
        "correct_answer": "The oldest stock is picked and dispatched first, reducing the risk of expiry or obsolescence"
    },
    {
        "question": "A Warehouse Management System (WMS) is used to:",
        "options": ["Manage employee payroll", "Control and optimise warehouse operations including receiving, storage, picking, packing and dispatch", "Process customer invoices", "Manage supplier contracts"],
        "correct_answer": "Control and optimise warehouse operations including receiving, storage, picking, packing and dispatch"
    },
    {
        "question": "Cross-docking in warehouse management refers to:",
        "options": ["Storing goods in multiple warehouse locations", "Transferring incoming goods directly to outbound vehicles with minimal or no storage time", "Conducting a full stock count", "Moving goods between warehouse zones"],
        "correct_answer": "Transferring incoming goods directly to outbound vehicles with minimal or no storage time"
    },
    {
        "question": "ABC analysis in warehouse management classifies inventory based on:",
        "options": ["Alphabetical order of product names", "The value and movement frequency of items — A items being highest value/fastest moving", "The physical size of products", "The supplier's location"],
        "correct_answer": "The value and movement frequency of items — A items being highest value/fastest moving"
    },
    {
        "question": "Cycle counting in a warehouse is performed to:",
        "options": ["Count all inventory once per year only", "Regularly verify the accuracy of inventory records by counting a subset of stock on a rotating basis", "Count only damaged goods", "Prepare the annual financial statements"],
        "correct_answer": "Regularly verify the accuracy of inventory records by counting a subset of stock on a rotating basis"
    },
    {
        "question": "Pick accuracy in warehouse operations refers to:",
        "options": ["The speed at which orders are picked", "The percentage of orders picked correctly without errors in item, quantity or location", "The number of pickers working per shift", "The distance travelled during the picking process"],
        "correct_answer": "The percentage of orders picked correctly without errors in item, quantity or location"
    },
    {
        "question": "Which technology trend is transforming modern warehouse operations?",
        "options": ["Manual paper-based picking systems", "Automation, robotics, barcode scanning and real-time inventory tracking systems", "Reducing warehouse size to cut costs", "Eliminating all technology to reduce complexity"],
        "correct_answer": "Automation, robotics, barcode scanning and real-time inventory tracking systems"
    },
    {
        "question": "Slotting in warehouse management refers to:",
        "options": ["Scheduling employee shifts", "Strategically assigning storage locations to products based on pick frequency, size and weight to optimise efficiency", "Allocating warehouse space to different customers", "Organising the loading dock schedule"],
        "correct_answer": "Strategically assigning storage locations to products based on pick frequency, size and weight to optimise efficiency"
    },
    {
        "question": "The receiving process in a warehouse typically includes:",
        "options": ["Only unloading goods from the delivery vehicle", "Unloading, inspecting, verifying against purchase orders, labelling and putting away goods into storage locations", "Immediately dispatching received goods to customers", "Only updating the inventory system"],
        "correct_answer": "Unloading, inspecting, verifying against purchase orders, labelling and putting away goods into storage locations"
    },
    {
        "question": "Order fulfilment accuracy is critical in warehouse management because:",
        "options": ["It reduces the need for warehouse staff", "Errors in picking and packing lead to customer dissatisfaction, returns, additional costs and reputational damage", "It increases the speed of all warehouse processes", "It eliminates the need for a WMS"],
        "correct_answer": "Errors in picking and packing lead to customer dissatisfaction, returns, additional costs and reputational damage"
    },
    {
        "question": "Safety in warehouse operations requires:",
        "options": ["Prioritising speed over all safety procedures", "Adhering to health and safety regulations, proper equipment use, clear signage and regular staff training", "Reducing the number of safety checks to improve efficiency", "Only applying safety rules to forklift operators"],
        "correct_answer": "Adhering to health and safety regulations, proper equipment use, clear signage and regular staff training"
    },
    {
        "question": "Reverse logistics in warehouse management involves:",
        "options": ["Moving goods from the warehouse to customers", "Managing the return of goods from customers back through the supply chain for reuse, repair, recycling or disposal", "Reversing incorrect stock entries in the WMS", "Moving goods between warehouse locations"],
        "correct_answer": "Managing the return of goods from customers back through the supply chain for reuse, repair, recycling or disposal"
    },
    {
        "question": "Key Performance Indicators (KPIs) commonly used in warehouse management include:",
        "options": ["Employee satisfaction and marketing ROI", "Order accuracy rate, inventory turnover, on-time dispatch and cost per order", "Company revenue and net profit margin", "Supplier payment terms and credit ratings"],
        "correct_answer": "Order accuracy rate, inventory turnover, on-time dispatch and cost per order"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "warehouse.*management", "$options": "i"}})
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
        "title": "Warehouse Management - Final Assessment",
        "description": "Test your knowledge of warehouse principles, processes, inventory management and modern warehouse trends. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
