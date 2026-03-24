import asyncio, os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def delete():
    result = await db.lessons.delete_many({'module_id': 'incoterms_2024_module_1'})
    print(f'Deleted {result.deleted_count} lessons')
    client.close()

asyncio.run(delete())
