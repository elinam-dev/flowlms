import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "International marketing differs from domestic marketing primarily because it involves:",
        "options": ["Selling only to English-speaking markets", "Adapting strategies to diverse cultural, economic, legal and competitive environments across multiple countries", "Using the same marketing mix globally without adaptation", "Focusing exclusively on digital channels"],
        "correct_answer": "Adapting strategies to diverse cultural, economic, legal and competitive environments across multiple countries"
    },
    {
        "question": "International market segmentation involves dividing global markets based on:",
        "options": ["Only geographic location", "Demographics, psychographics, behaviour and geographic factors to identify viable target segments", "Company size only", "The language spoken in each country"],
        "correct_answer": "Demographics, psychographics, behaviour and geographic factors to identify viable target segments"
    },
    {
        "question": "A product adaptation strategy in international marketing means:",
        "options": ["Selling the exact same product in all markets", "Modifying the product to meet the specific needs, preferences or regulations of a target market", "Reducing product quality to lower costs in developing markets", "Launching new products only in domestic markets first"],
        "correct_answer": "Modifying the product to meet the specific needs, preferences or regulations of a target market"
    },
    {
        "question": "Price discrimination in international markets refers to:",
        "options": ["Charging the same price in all markets", "Charging different prices in different markets based on local demand, competition and purchasing power", "Reducing prices only in developed markets", "Setting prices based solely on production costs"],
        "correct_answer": "Charging different prices in different markets based on local demand, competition and purchasing power"
    },
    {
        "question": "A global firm's success strategy typically involves:",
        "options": ["Ignoring local market differences", "Balancing global standardisation with local adaptation to achieve efficiency and market relevance", "Competing only on price", "Avoiding partnerships with local firms"],
        "correct_answer": "Balancing global standardisation with local adaptation to achieve efficiency and market relevance"
    },
    {
        "question": "A transnational strategy in international business aims to:",
        "options": ["Centralise all decisions at headquarters", "Achieve both global efficiency and local responsiveness simultaneously", "Focus only on cost reduction", "Operate exclusively in developed markets"],
        "correct_answer": "Achieve both global efficiency and local responsiveness simultaneously"
    },
    {
        "question": "A market orientation in international marketing means the firm:",
        "options": ["Focuses primarily on production efficiency", "Prioritises understanding and satisfying customer needs in each target market", "Sells whatever it produces regardless of demand", "Focuses only on competitor activities"],
        "correct_answer": "Prioritises understanding and satisfying customer needs in each target market"
    },
    {
        "question": "Global marketing research is conducted to:",
        "options": ["Confirm existing assumptions about international markets", "Gather accurate data on market size, customer behaviour, competition and environmental factors to support decisions", "Replace the need for local market knowledge", "Reduce the cost of entering new markets"],
        "correct_answer": "Gather accurate data on market size, customer behaviour, competition and environmental factors to support decisions"
    },
    {
        "question": "Market demand estimation in international markets involves:",
        "options": ["Using only historical domestic sales data", "Analysing population size, income levels, purchasing behaviour and market growth trends in the target country", "Assuming demand mirrors the home market", "Setting demand targets based on production capacity"],
        "correct_answer": "Analysing population size, income levels, purchasing behaviour and market growth trends in the target country"
    },
    {
        "question": "Supply chain management in an international context involves:",
        "options": ["Managing only domestic suppliers", "Coordinating the flow of goods, information and finances across global networks of suppliers, manufacturers and distributors", "Focusing exclusively on transportation costs", "Eliminating intermediaries from the supply chain"],
        "correct_answer": "Coordinating the flow of goods, information and finances across global networks of suppliers, manufacturers and distributors"
    },
    {
        "question": "Traditional forecasting methods in international supply chains include:",
        "options": ["Only AI-based predictive analytics", "Time series analysis, moving averages and expert judgement based on historical data", "Real-time IoT sensor data only", "Social media sentiment analysis exclusively"],
        "correct_answer": "Time series analysis, moving averages and expert judgement based on historical data"
    },
    {
        "question": "Which of the following is a key challenge in international supply chain management?",
        "options": ["Having too many local suppliers", "Managing currency fluctuations, customs regulations, lead time variability and geopolitical risks across borders", "Excess inventory in domestic warehouses", "Overly short supplier payment terms"],
        "correct_answer": "Managing currency fluctuations, customs regulations, lead time variability and geopolitical risks across borders"
    },
    {
        "question": "Positioning in international marketing refers to:",
        "options": ["The physical location of the company's offices", "How a brand or product is perceived relative to competitors in the minds of target customers in each market", "The logistics position of goods in transit", "The company's ranking on global stock exchanges"],
        "correct_answer": "How a brand or product is perceived relative to competitors in the minds of target customers in each market"
    },
    {
        "question": "Which entry mode gives a company the highest level of control in an international market but also carries the highest risk?",
        "options": ["Exporting", "Licensing", "Franchising", "Foreign Direct Investment (FDI)"],
        "correct_answer": "Foreign Direct Investment (FDI)"
    },
    {
        "question": "The integration of marketing and supply chain management in international business is important because:",
        "options": ["Marketing and supply chain operate completely independently", "Demand signals from marketing must align with supply chain capacity to ensure product availability, cost efficiency and customer satisfaction", "Supply chain decisions are made after all marketing campaigns are complete", "Marketing only affects domestic operations"],
        "correct_answer": "Demand signals from marketing must align with supply chain capacity to ensure product availability, cost efficiency and customer satisfaction"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "international.*marketing.*supply.*chain", "$options": "i"}})
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
        "title": "International Marketing and Supply Chain Management - Final Assessment",
        "description": "Test your knowledge of international marketing strategies, market research, segmentation and global supply chain management. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
