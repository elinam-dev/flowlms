"""
Simple script to update course lesson content
Usage: python update_lesson.py SALES-001 1 content.html
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def update_lesson(course_code, page_num, html_file):
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Read HTML content
    if not Path(html_file).exists():
        print(f"Error: File {html_file} not found")
        return
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find course
    course = await db.courses.find_one({"code": course_code})
    if not course:
        print(f"Error: Course {course_code} not found")
        client.close()
        return
    
    # Find module
    module = await db.modules.find_one({"course_id": course['id']})
    if not module:
        print(f"Error: No module found for course")
        client.close()
        return
    
    # Find lesson
    lesson = await db.lessons.find_one({
        "module_id": module['id'],
        "order": page_num - 1
    })
    
    if not lesson:
        print(f"Error: Lesson page {page_num} not found")
        client.close()
        return
    
    # Update lesson
    await db.lessons.update_one(
        {"id": lesson['id']},
        {"$set": {"content": html_content}}
    )
    
    print(f"✓ Updated: {course['title']} - Page {page_num}")
    print(f"  Lesson: {lesson['title']}")
    print(f"  Content length: {len(html_content)} characters")
    
    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python update_lesson.py <course_code> <page_num> <html_file>")
        print("Example: python update_lesson.py SALES-001 1 lesson1.html")
        sys.exit(1)
    
    course_code = sys.argv[1]
    page_num = int(sys.argv[2])
    html_file = sys.argv[3]
    
    asyncio.run(update_lesson(course_code, page_num, html_file))
