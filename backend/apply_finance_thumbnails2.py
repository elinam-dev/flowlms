import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

FOLDER = r"c:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\Finance"
BASE_URL = "http://localhost:8000/uploads/images/Finance"

# remaining 18 images in sorted order (excluding fundamentals_of_accounting.jpg already done)
images = sorted([f for f in os.listdir(FOLDER)
                 if os.path.isfile(os.path.join(FOLDER, f))
                 and f != "fundamentals_of_accounting.jpg"])
print("Images to rename:", images)

courses_map = [
    ("diploma in financial accounting",     "diploma_in_financial_accounting"),
    ("introduction to business accounting", "introduction_to_business_accounting"),
    ("essentials of throughput accounting", "essentials_of_throughput_accounting"),
    ("diploma in cost accounting",          "diploma_in_cost_accounting"),
    ("sage one",                            "sage_one"),
    ("the accounting cycle",                "the_accounting_cycle"),
    ("master the double-entry",             "master_the_double_entry"),
    ("tax accounting systems",              "tax_accounting_systems"),
    ("financial statement analysis",        "financial_statement_analysis"),
    ("cost and management accounting",      "cost_and_management_accounting"),
    ("diploma in decision making",          "diploma_in_decision_making"),
    ("accounts receive able",               "accounts_receivable_management"),
    ("accounts payable",                    "accounts_payable_management"),
    ("fundamentals of budgeting",           "fundamentals_of_budgeting"),
    ("essentials of sap",                   "essentials_of_sap"),
    ("basics of value",                     "basics_of_value_added_tax"),
    ("core excel skills",                   "core_excel_skills"),
    ("top 25 excel",                        "top_25_excel_formulas"),
]

async def main():
    for i, (search_term, new_name) in enumerate(courses_map):
        old_file = images[i]
        ext = os.path.splitext(old_file)[1]
        new_file = f"{new_name}{ext}"
        os.rename(os.path.join(FOLDER, old_file), os.path.join(FOLDER, new_file))
        thumbnail_url = f"{BASE_URL}/{new_file}"
        course = await db.courses.find_one({"title": {"$regex": search_term, "$options": "i"}})
        if course:
            await db.courses.update_one({"_id": course["_id"]}, {"$set": {"thumbnail": thumbnail_url}})
            print(f"OK: {old_file} -> {new_file} | {course['title']}")
        else:
            print(f"FAIL: {search_term}")

asyncio.run(main())
