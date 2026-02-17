import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def check_image_paths():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    course = await db.courses.find_one({'code': 'ENG-PUMP-002'})
    if course:
        module = await db.modules.find_one({'course_id': course['id']})
        lesson = await db.lessons.find_one({'module_id': module['id'], 'order': 0})
        print("Current content:")
        print(lesson['content'])
    
    client.close()

asyncio.run(check_image_paths())
