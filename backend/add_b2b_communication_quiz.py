import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Effective B2B communication differs from B2C communication primarily because:",
        "options": ["B2B involves emotional impulse buying", "B2B communication targets multiple decision-makers with longer sales cycles and rational, value-driven messaging", "B2B uses only digital channels", "B2B communication requires no relationship building"],
        "correct_answer": "B2B communication targets multiple decision-makers with longer sales cycles and rational, value-driven messaging"
    },
    {
        "question": "In B2B communication, understanding your audience means:",
        "options": ["Sending the same message to all contacts", "Identifying the roles, priorities and pain points of each stakeholder involved in the buying decision", "Focusing only on the final decision-maker", "Using technical jargon to demonstrate expertise"],
        "correct_answer": "Identifying the roles, priorities and pain points of each stakeholder involved in the buying decision"
    },
    {
        "question": "A value proposition in B2B communication should clearly communicate:",
        "options": ["The history and size of your company", "The specific benefits and measurable outcomes your product or service delivers to the client's business", "Your product's technical specifications only", "Your company's pricing structure"],
        "correct_answer": "The specific benefits and measurable outcomes your product or service delivers to the client's business"
    },
    {
        "question": "Active listening in B2B communication involves:",
        "options": ["Waiting for your turn to speak", "Fully concentrating, understanding and responding to what the other party is saying to build trust and uncover needs", "Taking notes without engaging with the speaker", "Agreeing with everything the client says"],
        "correct_answer": "Fully concentrating, understanding and responding to what the other party is saying to build trust and uncover needs"
    },
    {
        "question": "Which of the following is the most effective approach when handling objections in B2B communication?",
        "options": ["Dismiss the objection and redirect to your pitch", "Argue that the objection is incorrect", "Acknowledge the concern, ask clarifying questions and address it with relevant evidence or solutions", "Offer an immediate discount to overcome resistance"],
        "correct_answer": "Acknowledge the concern, ask clarifying questions and address it with relevant evidence or solutions"
    },
    {
        "question": "Professional written communication in B2B settings should be:",
        "options": ["Lengthy and detailed to show thoroughness", "Casual and informal to build rapport", "Clear, concise, structured and tailored to the recipient's needs and context", "Written in technical language to demonstrate expertise"],
        "correct_answer": "Clear, concise, structured and tailored to the recipient's needs and context"
    },
    {
        "question": "The primary purpose of a B2B business proposal is to:",
        "options": ["Describe your company's history in detail", "Persuade the prospective client that your solution addresses their specific needs and delivers measurable value", "List all available products and services", "Provide a standard price list"],
        "correct_answer": "Persuade the prospective client that your solution addresses their specific needs and delivers measurable value"
    },
    {
        "question": "Relationship management in B2B communication is important because:",
        "options": ["It eliminates the need for formal contracts", "Long-term business relationships drive repeat business, referrals and competitive advantage", "It reduces the need for product quality", "It allows businesses to charge higher prices without justification"],
        "correct_answer": "Long-term business relationships drive repeat business, referrals and competitive advantage"
    },
    {
        "question": "Non-verbal communication in B2B meetings includes:",
        "options": ["Only the words spoken during the meeting", "Body language, eye contact, posture and tone of voice, which significantly influence how messages are received", "Only written follow-up communications", "The agenda distributed before the meeting"],
        "correct_answer": "Body language, eye contact, posture and tone of voice, which significantly influence how messages are received"
    },
    {
        "question": "When presenting to a B2B client, the most effective structure is:",
        "options": ["Start with your company's achievements, then list product features", "Open with the client's challenge, present your solution and its benefits, then close with a clear call to action", "Present all technical details first, then discuss pricing", "Begin with pricing to establish budget alignment immediately"],
        "correct_answer": "Open with the client's challenge, present your solution and its benefits, then close with a clear call to action"
    },
    {
        "question": "Cross-cultural communication in B2B contexts requires:",
        "options": ["Using the same communication style with all international clients", "Awareness and respect for cultural differences in communication styles, business etiquette and decision-making processes", "Avoiding all cultural references in business communication", "Translating all documents into the client's language only"],
        "correct_answer": "Awareness and respect for cultural differences in communication styles, business etiquette and decision-making processes"
    },
    {
        "question": "Follow-up communication after a B2B meeting should:",
        "options": ["Be sent only if the client requests it", "Summarise key discussion points, agreed actions and next steps to maintain momentum and accountability", "Repeat the entire sales pitch", "Focus only on pricing and contract terms"],
        "correct_answer": "Summarise key discussion points, agreed actions and next steps to maintain momentum and accountability"
    },
    {
        "question": "Negotiation in B2B communication is most effective when it aims for:",
        "options": ["A win-lose outcome where your company maximises gains", "A win-win outcome where both parties achieve their key objectives", "The lowest possible price for the buyer", "A quick agreement regardless of terms"],
        "correct_answer": "A win-win outcome where both parties achieve their key objectives"
    },
    {
        "question": "Digital communication tools such as email and video conferencing in B2B settings require:",
        "options": ["Informal language to appear approachable", "The same level of professionalism, clarity and preparation as face-to-face communication", "Shorter messages with no context", "Avoiding any follow-up after digital meetings"],
        "correct_answer": "The same level of professionalism, clarity and preparation as face-to-face communication"
    },
    {
        "question": "The key to building credibility in B2B communication is:",
        "options": ["Making bold claims about your product's superiority", "Consistently delivering on promises, providing evidence-based information and demonstrating deep knowledge of the client's industry", "Using impressive corporate language in all communications", "Focusing exclusively on price competitiveness"],
        "correct_answer": "Consistently delivering on promises, providing evidence-based information and demonstrating deep knowledge of the client's industry"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "effective.*b2b.*communication", "$options": "i"}})
    if not course:
        course = await db.courses.find_one({"title": {"$regex": "b2b.*communication", "$options": "i"}})
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
        "title": "Effective B2B Communication - Final Assessment",
        "description": "Test your knowledge of B2B communication strategies, stakeholder engagement, proposals, negotiation and relationship management. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
