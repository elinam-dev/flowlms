import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def main():
    result = await db.courses.update_many({'category': 'finance'}, {'$set': {'category': 'Finance'}})
    print(f'Updated {result.modified_count} courses')

asyncio.run(main())
