import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE_URL = "http://localhost:8000/uploads/images/Finance"

courses_map = [
    ("fundamentals of accounting",          "fundamentals_of_accounting.jpg"),
    ("diploma in financial accounting",     "diploma_in_financial_accounting.jpg"),
    ("introduction to business accounting", "introduction_to_business_accounting.jpg"),
    ("essentials of throughput accounting", "essentials_of_throughput_accounting.jpg"),
    ("diploma in cost accounting",          "diploma_in_cost_accounting.jpg"),
    ("sage one",                            "sage_one.jpg"),
    ("the accounting cycle",                "the_accounting_cycle.jpg"),
    ("master the double-entry",             "master_the_double_entry.jpg"),
    ("tax accounting systems",              "tax_accounting_systems.jpg"),
    ("financial statement analysis",        "financial_statement_analysis.jpg"),
    ("cost and management accounting",      "cost_and_management_accounting.jpg"),
    ("diploma in decision making",          "diploma_in_decision_making.jpg"),
    ("accounts receive able",               "accounts_receivable_management.jpg"),
    ("accounts payable",                    "accounts_payable_management.jpg"),
    ("fundamentals of budgeting",           "fundamentals_of_budgeting.jpg"),
    ("essentials of sap",                   "essentials_of_sap.jpg"),
    ("basics of value",                     "basics_of_value_added_tax.jpg"),
    ("core excel skills",                   "core_excel_skills.jpg"),
    ("top 25 excel",                        "top_25_excel_formulas.jpg"),
]

async def main():
    for search_term, filename in courses_map:
        # handle .jpeg extension for screenshots
        folder = r"c:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\Finance"
        # check if .jpg exists, else try .jpeg
        if not os.path.exists(os.path.join(folder, filename)):
            filename = filename.replace('.jpg', '.jpeg')
        thumbnail_url = f"{BASE_URL}/{filename}"
        course = await db.courses.find_one({"title": {"$regex": search_term, "$options": "i"}})
        if course:
            await db.courses.update_one({"_id": course["_id"]}, {"$set": {"thumbnail": thumbnail_url}})
            print(f"OK: {course['title']} -> {filename}")
        else:
            print(f"FAIL: {search_term}")

asyncio.run(main())
