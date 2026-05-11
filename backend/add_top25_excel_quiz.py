import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "579d9692-fbb2-4193-8994-4d41a3298535"

QUESTIONS = [
    {
        "question": "The AND function in Excel returns TRUE only when:",
        "options": ["At least one argument is TRUE", "All arguments are TRUE", "The first argument is TRUE", "Any argument is FALSE"],
        "correct_answer": "All arguments are TRUE"
    },
    {
        "question": "The IFERROR function is used to:",
        "options": ["Generate an error message for debugging", "Return a specified value instead of an error if a formula produces an error result", "Check if a cell contains a formula", "Convert error values to zero automatically"],
        "correct_answer": "Return a specified value instead of an error if a formula produces an error result"
    },
    {
        "question": "The XOR function returns TRUE when:",
        "options": ["All arguments are TRUE", "All arguments are FALSE", "An odd number of arguments are TRUE", "Any one argument is TRUE"],
        "correct_answer": "An odd number of arguments are TRUE"
    },
    {
        "question": "The PV (Present Value) function in Excel calculates:",
        "options": ["The future value of an investment", "The current value of a series of future cash flows discounted at a given rate", "The monthly payment on a loan", "The net profit of an investment"],
        "correct_answer": "The current value of a series of future cash flows discounted at a given rate"
    },
    {
        "question": "The FV (Future Value) function calculates:",
        "options": ["The present value of future payments", "The value of an investment at the end of a period based on regular payments and a constant interest rate", "The interest rate required to reach a target value", "The number of periods needed to repay a loan"],
        "correct_answer": "The value of an investment at the end of a period based on regular payments and a constant interest rate"
    },
    {
        "question": "The PMT function in Excel is used to calculate:",
        "options": ["The present value of a bond", "The periodic payment required to repay a loan over a set number of periods at a given interest rate", "The yield on a bond investment", "The depreciation charge for a fixed asset"],
        "correct_answer": "The periodic payment required to repay a loan over a set number of periods at a given interest rate"
    },
    {
        "question": "The PPMT function calculates:",
        "options": ["The total payment on a loan for a given period", "The principal portion of a loan payment for a specific period", "The interest portion of a loan payment", "The future value of a series of payments"],
        "correct_answer": "The principal portion of a loan payment for a specific period"
    },
    {
        "question": "The PRICE function in Excel is used to calculate:",
        "options": ["The selling price of a product", "The price per $100 face value of a bond that pays periodic interest", "The market capitalisation of a company", "The net present value of a project"],
        "correct_answer": "The price per $100 face value of a bond that pays periodic interest"
    },
    {
        "question": "The YIELD function returns:",
        "options": ["The annual interest payment on a bond", "The yield of a security that pays periodic interest, given its price", "The maturity value of a bond", "The coupon rate set at issuance"],
        "correct_answer": "The yield of a security that pays periodic interest, given its price"
    },
    {
        "question": "The TEXT function in Excel is used to:",
        "options": ["Convert text to numbers", "Format a number as text using a specified format code", "Concatenate two text strings", "Count the number of characters in a cell"],
        "correct_answer": "Format a number as text using a specified format code"
    },
    {
        "question": "The CONCATENATE function (or & operator) in Excel is used to:",
        "options": ["Split text into separate columns", "Join two or more text strings into one", "Count the number of words in a cell", "Convert numbers to text format"],
        "correct_answer": "Join two or more text strings into one"
    },
    {
        "question": "The SUBSTITUTE function replaces:",
        "options": ["All values in a column with a new value", "A specific occurrence of a text string within another text string with a new string", "Blank cells with a default value", "Numbers with their text equivalents"],
        "correct_answer": "A specific occurrence of a text string within another text string with a new string"
    },
    {
        "question": "The SLN function in Excel calculates depreciation using:",
        "options": ["The declining balance method", "The straight-line method, spreading the cost evenly over the asset's useful life", "The sum-of-years-digits method", "The units of production method"],
        "correct_answer": "The straight-line method, spreading the cost evenly over the asset's useful life"
    },
    {
        "question": "The ACCRINTM function calculates:",
        "options": ["The accrued interest for a security that pays interest at maturity", "The monthly payment on a mortgage", "The present value of accrued expenses", "The accumulated depreciation on a fixed asset"],
        "correct_answer": "The accrued interest for a security that pays interest at maturity"
    },
    {
        "question": "The PROPER function in Excel converts text so that:",
        "options": ["All letters are uppercase", "All letters are lowercase", "The first letter of each word is capitalised and the rest are lowercase", "Numbers are converted to text"],
        "correct_answer": "The first letter of each word is capitalised and the rest are lowercase"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"id": COURSE_ID})
    if not course:
        print("Course not found")
        return
    print(f"Found: {course['title']}")
    module = await db.modules.find_one({"course_id": COURSE_ID})
    existing = await db.quizzes.find_one({"module_id": module["id"]})
    if existing:
        await db.quizzes.delete_one({"module_id": module["id"]})
        print("Removed existing quiz")
    await db.quizzes.insert_one({
        "id": str(uuid.uuid4()),
        "module_id": module["id"],
        "course_id": COURSE_ID,
        "title": "Top 25 Excel Formulas - Final Assessment",
        "description": "Test your knowledge of Excel's top financial, logical, text and lookup formulas. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
