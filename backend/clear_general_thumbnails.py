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

async def fix():
    titles = ['how to design performance', 'behavioral interviewing']
    for t in titles:
        await db.courses.update_one(
            {'title': {'$regex': t, '$options': 'i'}},
            {'$set': {'thumbnail': ''}}
        )
        c = await db.courses.find_one({'title': {'$regex': t, '$options': 'i'}}, {'_id': 0, 'title': 1, 'thumbnail': 1})
        print(f"Cleared: {c['title']}")

if __name__ == "__main__":
    asyncio.run(fix())
