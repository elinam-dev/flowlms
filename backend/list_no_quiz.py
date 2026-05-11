#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def check():
    courses = await db.courses.find({'is_published': True}, {'_id': 0, 'id': 1, 'title': 1, 'category': 1}).sort('category', 1).to_list(None)
    no_quiz = []
    has_quiz = []
    for c in courses:
        modules = await db.modules.find({'course_id': c['id']}).to_list(None)
        module_ids = [m['id'] for m in modules]
        quiz_count = await db.quizzes.count_documents({'module_id': {'$in': module_ids}}) if module_ids else 0
        if quiz_count == 0:
            no_quiz.append(f"[{c.get('category','?')}] {c['title']}")
        else:
            has_quiz.append(c['title'])

    print(f"WITHOUT QUIZ ({len(no_quiz)}):")
    for i, t in enumerate(no_quiz, 1):
        print(f"  {i:2}. {t}")
    print(f"\nWITH QUIZ ({len(has_quiz)}):")
    for t in has_quiz:
        print(f"  - {t}")

if __name__ == "__main__":
    asyncio.run(check())
