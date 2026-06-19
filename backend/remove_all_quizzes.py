import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def remove_all_quizzes():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    result = await db.quizzes.delete_many({})
    print(f"Deleted {result.deleted_count} quizzes")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(remove_all_quizzes())
