import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

QUESTIONS = [
    {
        "question": "Workplace diversity refers to:",
        "options": ["Hiring only employees from the same background", "The presence of differences among employees including race, gender, age, religion, disability, sexual orientation and cultural background", "Having employees with different job titles", "Offering a variety of employee benefits"],
        "correct_answer": "The presence of differences among employees including race, gender, age, religion, disability, sexual orientation and cultural background"
    },
    {
        "question": "Inclusion in the workplace means:",
        "options": ["Ensuring all employees look and think the same", "Creating an environment where all employees feel valued, respected and able to contribute fully regardless of their differences", "Including all employees in social events only", "Hiring a diverse workforce without any further action"],
        "correct_answer": "Creating an environment where all employees feel valued, respected and able to contribute fully regardless of their differences"
    },
    {
        "question": "Unconscious bias in the workplace refers to:",
        "options": ["Deliberate discrimination against a protected group", "Automatic, unintentional attitudes or stereotypes that affect decisions and behaviours without the person being aware", "A formal complaint raised by an employee", "A company policy that excludes certain groups"],
        "correct_answer": "Automatic, unintentional attitudes or stereotypes that affect decisions and behaviours without the person being aware"
    },
    {
        "question": "Workplace harassment is defined as:",
        "options": ["Any form of constructive feedback given to an employee", "Unwanted conduct related to a protected characteristic that has the purpose or effect of violating dignity or creating an intimidating, hostile or offensive environment", "Any disagreement between colleagues", "Performance management activities"],
        "correct_answer": "Unwanted conduct related to a protected characteristic that has the purpose or effect of violating dignity or creating an intimidating, hostile or offensive environment"
    },
    {
        "question": "A zero-tolerance policy on workplace harassment means:",
        "options": ["Minor incidents of harassment are tolerated if they are infrequent", "All forms of harassment are taken seriously, investigated promptly and result in appropriate disciplinary action", "Only physical harassment is addressed formally", "Harassment complaints are handled informally without documentation"],
        "correct_answer": "All forms of harassment are taken seriously, investigated promptly and result in appropriate disciplinary action"
    },
    {
        "question": "Respect in the workplace is demonstrated by:",
        "options": ["Only respecting senior management", "Treating all colleagues with dignity, listening actively, valuing different perspectives and maintaining professional conduct", "Agreeing with all colleagues at all times", "Avoiding all conflict regardless of the situation"],
        "correct_answer": "Treating all colleagues with dignity, listening actively, valuing different perspectives and maintaining professional conduct"
    },
    {
        "question": "Substance abuse in the workplace refers to:",
        "options": ["Only illegal drug use outside of work hours", "The use of alcohol, drugs or other substances that impairs an employee's ability to perform their job safely and effectively", "Excessive coffee consumption at work", "Use of prescription medication as directed by a doctor"],
        "correct_answer": "The use of alcohol, drugs or other substances that impairs an employee's ability to perform their job safely and effectively"
    },
    {
        "question": "An Employee Assistance Programme (EAP) in relation to substance abuse provides:",
        "options": ["Disciplinary action for employees with substance issues", "Confidential counselling, support and referral services to help employees address substance abuse and other personal challenges", "Drug testing services only", "Legal advice for employees facing criminal charges"],
        "correct_answer": "Confidential counselling, support and referral services to help employees address substance abuse and other personal challenges"
    },
    {
        "question": "A drug and alcohol policy in the workplace should include:",
        "options": ["Only the consequences of being caught under the influence", "Clear expectations, testing procedures, support mechanisms and consequences for violations", "Only information about illegal substances", "Only guidance for managers on how to identify substance abuse"],
        "correct_answer": "Clear expectations, testing procedures, support mechanisms and consequences for violations"
    },
    {
        "question": "The business case for diversity and inclusion includes:",
        "options": ["It is only a legal compliance requirement", "Diverse teams drive greater innovation, better decision-making, improved employee engagement and stronger business performance", "It only benefits large multinational companies", "It reduces the need for performance management"],
        "correct_answer": "Diverse teams drive greater innovation, better decision-making, improved employee engagement and stronger business performance"
    },
    {
        "question": "Bystander intervention in workplace harassment situations involves:",
        "options": ["Ignoring harassment to avoid conflict", "Taking action to safely interrupt, report or support a colleague who is experiencing harassment", "Only HR staff intervening in harassment situations", "Waiting for the victim to report the incident themselves"],
        "correct_answer": "Taking action to safely interrupt, report or support a colleague who is experiencing harassment"
    },
    {
        "question": "Cultural competence in a diverse workplace means:",
        "options": ["Speaking multiple languages fluently", "The ability to understand, communicate with and effectively interact with people from different cultural backgrounds", "Following only the dominant culture's norms", "Avoiding discussions about cultural differences"],
        "correct_answer": "The ability to understand, communicate with and effectively interact with people from different cultural backgrounds"
    },
    {
        "question": "Which of the following is an example of direct discrimination?",
        "options": ["Providing all employees with the same training opportunities", "Refusing to promote a qualified employee because of their religion", "Applying the same performance standards to all employees", "Offering flexible working arrangements to all staff"],
        "correct_answer": "Refusing to promote a qualified employee because of their religion"
    },
    {
        "question": "Reasonable accommodation for employees with disabilities means:",
        "options": ["Exempting disabled employees from all performance standards", "Making appropriate adjustments to the workplace or working arrangements to enable a disabled employee to perform their role effectively", "Providing only financial compensation to disabled employees", "Assigning disabled employees to less demanding roles without consultation"],
        "correct_answer": "Making appropriate adjustments to the workplace or working arrangements to enable a disabled employee to perform their role effectively"
    },
    {
        "question": "The foundation of a respectful workplace is built on:",
        "options": ["Strict rules and heavy penalties for misconduct only", "A culture of dignity, psychological safety, open communication and shared accountability for respectful behaviour at all levels", "Only senior leadership modelling respectful behaviour", "Annual diversity training with no follow-through"],
        "correct_answer": "A culture of dignity, psychological safety, open communication and shared accountability for respectful behaviour at all levels"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    course = await db.courses.find_one({"title": {"$regex": "respect foundations", "$options": "i"}})
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
        "title": "Respect Foundations: Diversity, Respect and Substance Abuse - Final Assessment",
        "description": "Test your knowledge of workplace diversity, inclusion, harassment prevention and substance abuse policies. You need 70% to pass.",
        "passing_score": 70,
        "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(QUESTIONS)]
    })
    print(f"Added quiz with {len(QUESTIONS)} questions to '{course['title']}'")
    client.close()

if __name__ == "__main__":
    asyncio.run(add())
