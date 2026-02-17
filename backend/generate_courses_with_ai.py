"""
AI-powered course content generator using Claude API
Generates detailed, professional course content for all courses
"""
import asyncio
import anthropic
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Get Claude API key from environment
CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
if not CLAUDE_API_KEY:
    print("ERROR: CLAUDE_API_KEY not found in .env file")
    print("Get your API key from: https://console.anthropic.com/")
    exit(1)

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

async def generate_lesson_content(course_title, category, page_num, total_pages, lesson_title):
    """Generate detailed lesson content using Claude API"""
    
    prompt = f"""You are an expert instructional designer creating professional online course content for a corporate LMS.

Course: {course_title}
Category: {category}
Lesson: Page {page_num} of {total_pages} - {lesson_title}

Create detailed, educational content for this lesson page. The content should be:
- Professional and in-depth (800-1200 words)
- Include specific examples, data, and real-world applications
- Use proper HTML formatting with semantic tags
- Include tables, lists, and highlight boxes where appropriate
- Be unique and avoid generic statements
- Focus on practical, actionable knowledge

Use these HTML classes for styling:
- <div class="lesson-content"> for wrapper
- <div class="highlight-box"> for important points
- <div class="info-box"> for additional information
- <div class="example-box"> for examples and case studies
- <div class="responsibilities-grid"> with <div class="resp-card"> for grid layouts
- <table> for data and comparisons

Generate ONLY the HTML content (no markdown, no code blocks, just raw HTML)."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        print(f"  Error generating content: {e}")
        return f"<div class='lesson-content'><h2>{lesson_title}</h2><p>Content generation failed. Please try again.</p></div>"

async def generate_quiz_questions(course_title, category):
    """Generate quiz questions using Claude API"""
    
    prompt = f"""Create 12 quiz questions for the course: {course_title} (Category: {category})

Generate a mix of:
- 6 multiple choice questions (4 options each)
- 3 true/false questions
- 3 short answer questions

Questions should test deep understanding, not just memorization.

Return ONLY a JSON array in this exact format:
[
  {{"question": "...", "type": "multiple_choice", "options": ["A", "B", "C", "D"], "correct_answer": "A"}},
  {{"question": "...", "type": "true_false", "correct_answer": "true"}},
  {{"question": "...", "type": "short_answer", "correct_answer": "..."}}
]"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        content = message.content[0].text.strip()
        # Extract JSON if wrapped in code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        print(f"  Error generating quiz: {e}")
        return []

async def get_lesson_titles(course_title, category, num_pages):
    """Generate contextual lesson titles using Claude API"""
    
    prompt = f"""Generate {num_pages} lesson titles for the course: {course_title} (Category: {category})

Create a logical progression from beginner to advanced topics.
Each title should be specific and descriptive (not generic).

Return ONLY a JSON array of strings:
["Title 1", "Title 2", "Title 3", ...]"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        content = message.content[0].text.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        print(f"  Error generating titles: {e}")
        return [f"Lesson {i+1}" for i in range(num_pages)]

async def regenerate_course_content(course_code=None, batch_size=5):
    """Regenerate course content with AI-generated material"""
    
    mongo_url = os.environ['MONGO_URL']
    db_client = AsyncIOMotorClient(mongo_url)
    db = db_client[os.environ['DB_NAME']]
    
    # Get courses to process
    query = {"code": course_code} if course_code else {}
    courses = await db.courses.find(query).to_list(None)
    
    if not courses:
        print("No courses found")
        return
    
    print(f"\n{'='*80}")
    print(f"AI Course Content Generator")
    print(f"{'='*80}")
    print(f"Found {len(courses)} course(s) to process")
    print(f"Processing in batches of {batch_size}")
    print(f"{'='*80}\n")
    
    for idx, course in enumerate(courses, 1):
        print(f"\n[{idx}/{len(courses)}] Processing: {course['title']}")
        print(f"  Category: {course.get('category', 'N/A')}")
        print(f"  Code: {course.get('code', 'N/A')}")
        
        # Get module
        module = await db.modules.find_one({"course_id": course['id']})
        if not module:
            print("  ⚠ No module found, skipping")
            continue
        
        # Count existing lessons
        lesson_count = await db.lessons.count_documents({"module_id": module['id']})
        print(f"  Current lessons: {lesson_count}")
        
        # Determine target page count based on category
        page_counts = {
            "FINANCE": 60, "ENGINEERING": 58, "SALES": 55, "HUMAN RESOURCES": 52,
            "SUPPLY CHAIN": 50, "MANAGEMENT": 48, "HEALTH & SAFETY": 45,
            "PERSONAL DEVELOPMENT": 40, "POLICY": 38, "LANGUAGE": 35
        }
        target_pages = page_counts.get(course.get('category', ''), 45)
        
        # Generate lesson titles
        print(f"  Generating {target_pages} lesson titles...")
        lesson_titles = await get_lesson_titles(course['title'], course.get('category', ''), target_pages)
        
        # Delete existing lessons
        await db.lessons.delete_many({"module_id": module['id']})
        print(f"  Deleted old lessons")
        
        # Generate new lessons
        print(f"  Generating {target_pages} detailed lessons...")
        for page_num in range(1, target_pages + 1):
            lesson_title = lesson_titles[page_num - 1] if page_num <= len(lesson_titles) else f"Lesson {page_num}"
            
            print(f"    [{page_num}/{target_pages}] {lesson_title[:50]}...")
            
            content = await generate_lesson_content(
                course['title'],
                course.get('category', ''),
                page_num,
                target_pages,
                lesson_title
            )
            
            await db.lessons.insert_one({
                "id": str(__import__('uuid').uuid4()),
                "module_id": module['id'],
                "title": f"Page {page_num}: {lesson_title}",
                "content_type": "text",
                "content": content,
                "duration_minutes": 15,
                "order": page_num - 1
            })
        
        # Generate quiz
        print(f"  Generating quiz questions...")
        quiz_questions = await generate_quiz_questions(course['title'], course.get('category', ''))
        
        # Delete existing quiz
        await db.quizzes.delete_many({"module_id": module['id']})
        
        # Create new quiz
        if quiz_questions:
            await db.quizzes.insert_one({
                "id": str(__import__('uuid').uuid4()),
                "module_id": module['id'],
                "title": f"{course['title']} - Final Assessment",
                "description": f"Test your knowledge of {course['title']}. You need 70% to pass.",
                "passing_score": 70,
                "questions": quiz_questions,
                "time_limit_minutes": 30,
                "created_at": "2024-01-01T00:00:00"
            })
            print(f"  ✓ Quiz created with {len(quiz_questions)} questions")
        
        print(f"  ✓ Course regenerated with {target_pages} pages")
        
        # Batch control
        if idx % batch_size == 0 and idx < len(courses):
            print(f"\n{'='*80}")
            print(f"Completed batch {idx//batch_size}. Processed {idx}/{len(courses)} courses")
            print(f"{'='*80}\n")
    
    print(f"\n{'='*80}")
    print(f"✅ All courses processed successfully!")
    print(f"{'='*80}\n")
    
    db_client.close()

if __name__ == "__main__":
    import sys
    
    # Usage: python generate_courses_with_ai.py [course_code] [batch_size]
    course_code = sys.argv[1] if len(sys.argv) > 1 else None
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    asyncio.run(regenerate_course_content(course_code, batch_size))
