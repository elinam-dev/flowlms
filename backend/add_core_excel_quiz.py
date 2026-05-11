import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"
COURSE_ID = "ddafd679-00f1-4b08-bbd2-00246952a4c3"

QUESTIONS = [
    {
        "question": "The VLOOKUP function in Excel searches for a value in:",
        "options": ["Any column of a table", "The leftmost column of a table and returns a value from a specified column to the right", "The top row of a table", "Multiple tables simultaneously"],
        "correct_answer": "The leftmost column of a table and returns a value from a specified column to the right"
    },
    {
        "question": "The main advantage of INDEX and MATCH over VLOOKUP is:",
        "options": ["INDEX and MATCH is easier to write", "INDEX and MATCH can look up values in any direction and is not limited to the leftmost column", "VLOOKUP cannot handle text values", "INDEX and MATCH only works with numbers"],
        "correct_answer": "INDEX and MATCH can look up values in any direction and is not limited to the leftmost column"
    },
    {
        "question": "XLOOKUP improves on VLOOKUP by:",
        "options": ["Only working with sorted data", "Searching in any direction, returning multiple columns and handling errors more gracefully", "Being limited to exact matches only", "Requiring the lookup column to be the first column"],
        "correct_answer": "Searching in any direction, returning multiple columns and handling errors more gracefully"
    },
    {
        "question": "The SUMIF function is used to:",
        "options": ["Sum all values in a range regardless of criteria", "Sum values in a range that meet a single specified condition", "Count cells that meet multiple criteria", "Average values based on a condition"],
        "correct_answer": "Sum values in a range that meet a single specified condition"
    },
    {
        "question": "An IF statement in Excel returns:",
        "options": ["Always a numeric value", "One value if a condition is TRUE and another value if the condition is FALSE", "The sum of a range of cells", "The average of values in a column"],
        "correct_answer": "One value if a condition is TRUE and another value if the condition is FALSE"
    },
    {
        "question": "A Pivot Table in Excel is primarily used to:",
        "options": ["Create complex formulas automatically", "Summarise, analyse and explore large datasets interactively without writing formulas", "Format cells with conditional colours", "Protect worksheets from editing"],
        "correct_answer": "Summarise, analyse and explore large datasets interactively without writing formulas"
    },
    {
        "question": "Excel Tables (created with Ctrl+T) offer which key advantage for accountants?",
        "options": ["They prevent any changes to the data", "They automatically expand to include new rows and columns, and structured references update formulas dynamically", "They convert all data to text format", "They remove duplicate values automatically"],
        "correct_answer": "They automatically expand to include new rows and columns, and structured references update formulas dynamically"
    },
    {
        "question": "The FILTER function in Excel (dynamic arrays) allows you to:",
        "options": ["Sort data alphabetically only", "Extract a subset of data from a range based on specified criteria, spilling results automatically", "Remove blank cells from a range", "Apply conditional formatting to a dataset"],
        "correct_answer": "Extract a subset of data from a range based on specified criteria, spilling results automatically"
    },
    {
        "question": "The UNIQUE function in Excel returns:",
        "options": ["The largest value in a range", "A list of distinct values from a range, removing duplicates automatically", "The count of unique values only", "Values sorted in ascending order"],
        "correct_answer": "A list of distinct values from a range, removing duplicates automatically"
    },
    {
        "question": "Dynamic array functions in Excel differ from traditional formulas because they:",
        "options": ["Can only be used in Excel 2010 and earlier", "Automatically spill results into multiple cells without needing to be entered as array formulas with Ctrl+Shift+Enter", "Only work with numerical data", "Require manual updating when source data changes"],
        "correct_answer": "Automatically spill results into multiple cells without needing to be entered as array formulas with Ctrl+Shift+Enter"
    },
    {
        "question": "A logical test in Excel evaluates to:",
        "options": ["A number between 0 and 100", "Either TRUE or FALSE", "A text string", "A date value"],
        "correct_answer": "Either TRUE or FALSE"
    },
    {
        "question": "The SORTBY function in Excel allows you to sort a range based on:",
        "options": ["Only one column at a time", "One or more separate arrays or columns, even if they are not part of the original range", "Alphabetical order only", "The cell colour"],
        "correct_answer": "One or more separate arrays or columns, even if they are not part of the original range"
    },
    {
        "question": "For an accountant, which Excel skill is most critical for reconciling large datasets from different sources?",
        "options": ["Changing font colours", "Using VLOOKUP, INDEX/MATCH or XLOOKUP to match and compare data across tables", "Creating pie charts", "Inserting page breaks for printing"],
        "correct_answer": "Using VLOOKUP, INDEX/MATCH or XLOOKUP to match and compare data across tables"
    },
    {
        "question": "SUMIFS differs from SUMIF in that it:",
        "options": ["Can only sum one column", "Allows multiple criteria across multiple ranges to be applied simultaneously", "Only works with text criteria", "Sums values based on a single condition"],
        "correct_answer": "Allows multiple criteria across multiple ranges to be applied simultaneously"
    },
    {
        "question": "Which of the following best describes a structured reference in an Excel Table?",
        "options": ["A reference using absolute cell addresses like $A$1", "A reference that uses the table and column name (e.g. Table1[Amount]) making formulas easier to read and maintain", "A reference to a named range outside the table", "A reference that only works in Pivot Tables"],
        "correct_answer": "A reference that uses the table and column name (e.g. Table1[Amount]) making formulas easier to read and maintain"
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
        "title": "Core Excel Skills for Accountants - Final Assessment",
        "description": "Test your practical Excel skills including lookups, IF statements, Pivot Tables and dynamic array functions. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
