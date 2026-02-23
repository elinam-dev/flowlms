import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

async def update():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    course = await db.courses.find_one({"title": "Motivation - Power Guide to motivating yourself and others"})
    
    questions = [
        {
            "question": "Want-Power Creates Will-Power",
            "type": "true_false",
            "correct_answer": "true"
        },
        {
            "question": "Our Beliefs Are Typically A _________ Match With Our Close Friends",
            "type": "multiple_choice",
            "options": ["47%", "90%", "70%", "25%"],
            "correct_answer": "90%"
        },
        {
            "question": "People are ALWAYS Motivated",
            "type": "true_false",
            "correct_answer": "false"
        },
        {
            "question": "Self-Image is Just an IDEA in Your Head",
            "type": "true_false",
            "correct_answer": "true"
        },
        {
            "question": "One Definition of \"motivation\" is: \"A Mental Force that induces an Action\"",
            "type": "true_false",
            "correct_answer": "true"
        },
        {
            "question": "We Make up our \"Reality\" as we go along",
            "type": "true_false",
            "correct_answer": "true"
        },
        {
            "question": "\"If You Want to Change The Whole World … Change The Way You Look At It\"",
            "type": "true_false",
            "correct_answer": "true"
        },
        {
            "question": "Another Definition of \"Motivation\" is: \"A Mental Strategy\"",
            "type": "true_false",
            "correct_answer": "true"
        },
        {
            "question": "Self-Image is Just a STORY we have about ourselves",
            "type": "true_false",
            "correct_answer": "true"
        },
        {
            "question": "We never go HIGHER or LOWER than our STANDARDS",
            "type": "true_false",
            "correct_answer": "true"
        }
    ]
    
    await db.quizzes.update_one(
        {"course_id": course["id"]},
        {"$set": {"questions": questions, "title": "Motivation Final Assessment"}}
    )
    
    print("Updated quiz with 10 questions")
    client.close()

if __name__ == "__main__":
    asyncio.run(update())
