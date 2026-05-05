#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def add_quiz():
    course = await db.courses.find_one(
        {'title': {'$regex': 'pump types', '$options': 'i'}},
        {'_id': 0, 'id': 1, 'title': 1}
    )
    print(f"Found: {course['title']}")

    module = await db.modules.find_one({'course_id': course['id']})

    questions = [
        {"question": "What is the primary function of a pump?", "options": ["To generate heat", "To move liquid by adding energy", "To store liquid", "To filter liquid"], "correct_answer": "To move liquid by adding energy"},
        {"question": "A pump converts mechanical energy into:", "options": ["Electrical energy", "Thermal energy", "Hydraulic energy", "Chemical energy"], "correct_answer": "Hydraulic energy"},
        {"question": "Which component provides the rotational energy to drive a pump?", "options": ["Shaft", "Bearing", "Motor", "Impeller"], "correct_answer": "Motor"},
        {"question": "Flow rate refers to:", "options": ["Height of liquid lifted", "Quantity of liquid per unit time", "Force acting on liquid", "Speed of the motor"], "correct_answer": "Quantity of liquid per unit time"},
        {"question": "Pump head is best described as:", "options": ["The force applied to the pump", "The height a pump can lift liquid", "The weight of the liquid", "The pump speed"], "correct_answer": "The height a pump can lift liquid"},
        {"question": "Pressure in a pumping system is defined as:", "options": ["Speed of liquid", "Height of liquid", "Force per unit area", "Volume of liquid"], "correct_answer": "Force per unit area"},
        {"question": "Which side of the pump is the suction side?", "options": ["The outlet side", "The inlet side", "The motor side", "The coupling side"], "correct_answer": "The inlet side"},
        {"question": "The discharge side of a pump always has:", "options": ["The lowest pressure", "No pressure", "The highest pressure", "Atmospheric pressure only"], "correct_answer": "The highest pressure"},
        {"question": "Static head depends mainly on:", "options": ["Flow rate", "Pipe diameter", "Vertical height difference", "Pump speed"], "correct_answer": "Vertical height difference"},
        {"question": "Dynamic head includes:", "options": ["Only vertical lift", "Only friction losses", "Static head plus all system losses", "Only discharge pressure"], "correct_answer": "Static head plus all system losses"},
        {"question": "TDH stands for:", "options": ["Total Displacement Height", "Total Dynamic Head", "Theoretical Discharge Head", "Total Drive Horsepower"], "correct_answer": "Total Dynamic Head"},
        {"question": "NPSH is mainly associated with:", "options": ["Motor power", "Pump discharge", "Pump suction condition", "Bearing lubrication"], "correct_answer": "Pump suction condition"},
        {"question": "NPSHr means:", "options": ["Net Pump Speed Rating", "Net Positive Suction Head Required", "Net Pressure Supply at Housing", "Net Pump Safety Height"], "correct_answer": "Net Positive Suction Head Required"},
        {"question": "For safe pump operation:", "options": ["NPSHa must be equal to zero", "NPSHr must be greater than NPSHa", "NPSHa must be greater than NPSHr", "NPSHa must be ignored"], "correct_answer": "NPSHa must be greater than NPSHr"},
        {"question": "Cavitation occurs due to:", "options": ["High discharge pressure", "Low suction pressure", "High motor current", "Oversized pipes"], "correct_answer": "Low suction pressure"},
        {"question": "Which of the following is a common symptom of cavitation?", "options": ["Silent operation", "Smooth vibration-free running", "Noise like stones inside the pump", "Increased efficiency"], "correct_answer": "Noise like stones inside the pump"},
        {"question": "Which condition can lead to cavitation?", "options": ["Short suction line", "Large suction pipe", "Blocked suction strainer", "High NPSH available"], "correct_answer": "Blocked suction strainer"},
        {"question": "Pump efficiency represents:", "options": ["Pump speed", "Flow capacity", "Ratio of useful output power to input power", "Pump weight"], "correct_answer": "Ratio of useful output power to input power"},
        {"question": "The Best Efficiency Point (BEP) is:", "options": ["The maximum power point", "The most efficient and stable operating point", "The lowest pressure point", "The shutdown point"], "correct_answer": "The most efficient and stable operating point"},
        {"question": "Operating a pump too far away from BEP causes:", "options": ["Lower vibration", "Reduced wear", "Increased vibration and failures", "Higher efficiency"], "correct_answer": "Increased vibration and failures"},
        {"question": "Which of the following is the lowest pressure point in a pump?", "options": ["Discharge flange", "Suction flange", "Bearing housing", "Motor terminal box"], "correct_answer": "Suction flange"},
        {"question": "A pump is selected mainly based on:", "options": ["Motor size only", "Suction pipe size only", "Required flow and total dynamic head", "Pump color and brand"], "correct_answer": "Required flow and total dynamic head"},
        {"question": "Which of the following is NOT a form of energy added to liquid by a pump?", "options": ["Velocity energy", "Pressure energy", "Potential (head) energy", "Electrical energy"], "correct_answer": "Electrical energy"},
        {"question": "Which of the following is a basic cause of pump failure?", "options": ["Proper alignment", "Correct NPSH", "Dry running", "Good lubrication"], "correct_answer": "Dry running"},
        {"question": "Which statement is TRUE about pumps?", "options": ["Pumps create liquid", "Pumps store energy", "Pumps transfer energy to liquid", "Pumps destroy energy"], "correct_answer": "Pumps transfer energy to liquid"},
    ]

    quiz_id = str(uuid.uuid4())
    await db.quizzes.insert_one({
        "id": quiz_id,
        "module_id": module["id"],
        "course_id": course["id"],
        "title": "Pump Types - Final Assessment",
        "description": "Test your knowledge of pump types, principles and operations. You need 70% to pass.",
        "passing_score": 70,
        "questions": [
            {
                "question": q["question"],
                "question_type": "multiple_choice",
                "options": q["options"],
                "correct_answer": q["correct_answer"],
                "points": 1,
                "order": i
            }
            for i, q in enumerate(questions)
        ]
    })

    print(f"Added quiz with {len(questions)} questions to '{course['title']}'")

if __name__ == "__main__":
    asyncio.run(add_quiz())
