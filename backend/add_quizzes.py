"""
Add quizzes to all courses
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
import random

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def add_quizzes():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Get all courses
    courses = await db.courses.find({}).to_list(1000)
    
    for course in courses:
        print(f"Adding quiz to: {course['title']}")
        
        # Get first module
        modules = await db.modules.find({"course_id": course["id"]}).to_list(100)
        if not modules:
            print(f"  No modules found, skipping")
            continue
        
        module = modules[0]
        
        # Check if quiz already exists
        existing_quiz = await db.quizzes.find_one({"module_id": module["id"]})
        if existing_quiz:
            print(f"  Quiz already exists, skipping")
            continue
        
        # Determine question count based on course
        if course['course_type'] == 'compulsory':
            num_questions = 10
        else:
            num_questions = random.choice([10, 12, 15])
        
        # Generate quiz
        quiz_id = str(uuid.uuid4())
        questions = generate_questions(course['title'], course['category'], num_questions)
        
        await db.quizzes.insert_one({
            "id": quiz_id,
            "module_id": module["id"],
            "title": f"{course['title']} - Final Assessment",
            "description": f"Test your knowledge of {course['title']}. You need {70}% to pass.",
            "passing_score": 70,
            "questions": questions,
            "time_limit_minutes": num_questions * 2,
            "created_at": "2024-01-01T00:00:00"
        })
        
        print(f"  ✓ Added quiz with {num_questions} questions")
    
    print(f"\n✅ Quizzes added to all courses!")
    client.close()

def generate_questions(course_title, category, num_questions):
    """Generate contextual quiz questions"""
    questions = []
    
    # Question templates based on category
    if category == "HR Policy":
        templates = [
            ("What is the maximum number of annual leave days?", ["12 days", "15 days", "18 days", "21 days"], "18 days"),
            ("Who approves leave requests?", ["HR Manager", "Direct Supervisor", "CEO", "Team Lead"], "Direct Supervisor"),
            ("How many days notice for annual leave?", ["3 days", "5 days", "7 days", "14 days"], "14 days"),
            ("What is sick leave entitlement?", ["5 days", "10 days", "15 days", "20 days"], "10 days"),
            ("Maternity leave duration?", ["8 weeks", "12 weeks", "14 weeks", "16 weeks"], "14 weeks"),
            ("Who handles disciplinary issues?", ["HR Department", "Manager", "CEO", "Team"], "HR Department"),
            ("What requires written warning?", ["Late arrival", "Serious misconduct", "Minor errors", "All issues"], "Serious misconduct"),
            ("Leave request submission method?", ["Email", "Leave form", "Verbal", "Text"], "Leave form"),
            ("Emergency leave approval?", ["Immediate", "24 hours", "3 days", "1 week"], "Immediate"),
            ("Annual leave carry over?", ["Not allowed", "5 days max", "10 days max", "Unlimited"], "5 days max"),
        ]
    elif category == "Ethics":
        templates = [
            ("What defines ethical behavior?", ["Following rules", "Honesty and integrity", "Profit focus", "Speed"], "Honesty and integrity"),
            ("How to handle conflicts of interest?", ["Ignore them", "Disclose immediately", "Hide them", "Delay reporting"], "Disclose immediately"),
            ("Gift acceptance policy?", ["Accept all", "Refuse all", "Report and assess", "Keep secret"], "Report and assess"),
            ("Confidential information handling?", ["Share freely", "Protect strictly", "Sell it", "Post online"], "Protect strictly"),
            ("Reporting unethical behavior?", ["Ignore it", "Report to supervisor", "Join in", "Keep quiet"], "Report to supervisor"),
            ("Professional conduct standard?", ["Casual", "Strict professionalism", "Flexible", "No standard"], "Strict professionalism"),
            ("Customer data protection?", ["Optional", "Mandatory", "Flexible", "Not needed"], "Mandatory"),
            ("Workplace harassment policy?", ["Tolerated", "Zero tolerance", "Case by case", "Ignored"], "Zero tolerance"),
            ("Ethical decision making?", ["Quick choices", "Consider impact", "Profit first", "Speed matters"], "Consider impact"),
            ("Code of conduct applies to?", ["Some staff", "All employees", "Managers only", "Optional"], "All employees"),
        ]
    elif category == "Safety":
        templates = [
            ("PPE stands for?", ["Personal Protection Equipment", "Private Property Entry", "Public Place Entry", "None"], "Personal Protection Equipment"),
            ("Who is responsible for safety?", ["Safety officer only", "Everyone", "Manager only", "HR only"], "Everyone"),
            ("Fire extinguisher color for electrical?", ["Red", "Blue", "Black", "Yellow"], "Black"),
            ("Emergency assembly point?", ["Parking lot", "Designated area", "Office", "Anywhere"], "Designated area"),
            ("Report accidents within?", ["24 hours", "Immediately", "1 week", "1 month"], "Immediately"),
            ("Safety training frequency?", ["Once", "Annually", "Never", "Optional"], "Annually"),
            ("First aid kit location?", ["Hidden", "Clearly marked", "Manager office", "Unknown"], "Clearly marked"),
            ("Hazard reporting to?", ["No one", "Supervisor", "Ignore", "Later"], "Supervisor"),
            ("Safety equipment inspection?", ["Never", "Regularly", "Rarely", "Optional"], "Regularly"),
            ("Emergency evacuation priority?", ["Equipment", "People safety", "Documents", "Money"], "People safety"),
        ]
    else:  # SALES (ENGINEER)
        templates = [
            ("Primary focus in B2B sales?", ["Price only", "Customer needs", "Quick close", "Volume"], "Customer needs"),
            ("Best way to handle objections?", ["Argue", "Listen and address", "Ignore", "Give up"], "Listen and address"),
            ("Flowitec specializes in?", ["Software", "Pumps and valves", "Construction", "Food"], "Pumps and valves"),
            ("Key to customer retention?", ["Low price", "Relationship building", "Pressure", "Discounts"], "Relationship building"),
            ("Technical knowledge importance?", ["Not needed", "Critical for credibility", "Optional", "Minimal"], "Critical for credibility"),
            ("Proposal should focus on?", ["Features only", "Value and ROI", "Price only", "Competition"], "Value and ROI"),
            ("Follow-up timing?", ["Never", "Promptly as promised", "Months later", "Random"], "Promptly as promised"),
            ("Negotiation goal?", ["Win at all costs", "Win-win solution", "Lowest price", "Quick deal"], "Win-win solution"),
            ("CRM system purpose?", ["Optional tool", "Track customer interactions", "Waste time", "Not needed"], "Track customer interactions"),
            ("Sales presentation focus?", ["Company history", "Customer benefits", "Technical specs", "Price list"], "Customer benefits"),
            ("Closing technique?", ["Pressure tactics", "Assumptive close", "Begging", "Threats"], "Assumptive close"),
            ("Account management priority?", ["New customers only", "Existing relationships", "Ignore accounts", "Price cuts"], "Existing relationships"),
            ("Product knowledge source?", ["Guessing", "Training and manuals", "Competitors", "Internet only"], "Training and manuals"),
            ("Customer needs analysis?", ["Skip it", "Essential first step", "After sale", "Not important"], "Essential first step"),
            ("Sales ethics importance?", ["Not important", "Fundamental", "Flexible", "Optional"], "Fundamental"),
        ]
    
    # Select random questions
    selected = random.sample(templates, min(num_questions, len(templates)))
    
    for i, (question, options, answer) in enumerate(selected):
        questions.append({
            "question": question,
            "question_type": "multiple_choice",
            "options": options,
            "correct_answer": answer,
            "points": 1,
            "order": i
        })
    
    return questions

if __name__ == "__main__":
    asyncio.run(add_quizzes())
