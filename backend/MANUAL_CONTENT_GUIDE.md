# Manual Course Content Improvement Guide

Use free AI tools to create detailed course content without spending money.

## Free AI Tools

1. **ChatGPT Free** - https://chat.openai.com (GPT-3.5)
2. **Claude.ai Free** - https://claude.ai (Limited messages/day)
3. **Google Gemini** - https://gemini.google.com (Free)
4. **Perplexity AI** - https://perplexity.ai (Free with limits)

## Step-by-Step Process

### 1. Get Course List
```bash
cd backend
python -c "
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
load_dotenv()

async def list_courses():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    courses = await db.courses.find({}, {'_id': 0, 'title': 1, 'code': 1, 'category': 1}).to_list(None)
    for c in courses:
        print(f\"{c['code']}: {c['title']} ({c['category']})\")
    client.close()

asyncio.run(list_courses())
"
```

### 2. Generate Content with AI

Copy this prompt to ChatGPT/Claude:

```
I need detailed educational content for an online course lesson.

Course: [COURSE TITLE]
Category: [CATEGORY]
Lesson: Page [X] of 30 - [LESSON TITLE]

Create professional, in-depth content (800-1000 words) that includes:
- Specific examples and real-world applications
- Data, statistics, or formulas where relevant
- Practical exercises or scenarios
- Tables or lists for key information
- Case studies or examples

Format as HTML using these classes:
- <div class="lesson-content"> wrapper
- <div class="highlight-box"> for important points
- <div class="info-box"> for additional info
- <div class="example-box"> for examples
- <table> for data
- <div class="responsibilities-grid"> with <div class="resp-card"> for grids

Generate ONLY the HTML content.
```

### 3. Update Database

Save the generated HTML to a file, then run:

```python
# update_lesson.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def update_lesson(course_code, page_num, html_content):
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Find course
    course = await db.courses.find_one({"code": course_code})
    if not course:
        print(f"Course {course_code} not found")
        return
    
    # Find module
    module = await db.modules.find_one({"course_id": course['id']})
    
    # Find lesson
    lesson = await db.lessons.find_one({
        "module_id": module['id'],
        "order": page_num - 1
    })
    
    if lesson:
        await db.lessons.update_one(
            {"id": lesson['id']},
            {"$set": {"content": html_content}}
        )
        print(f"✓ Updated {course['title']} - Page {page_num}")
    
    client.close()

# Usage
html = """<div class="lesson-content">
[PASTE YOUR GENERATED HTML HERE]
</div>"""

asyncio.run(update_lesson("SALES-001", 1, html))
```

## Priority Courses to Improve

Focus on these high-value courses first:

### Top 10 Priority:
1. Introduction to International Commercial Terms (Incoterms)
2. Diploma in Sales Management
3. Diploma in Financial Accounting
4. Diploma in Supply Chain Management
5. Diploma in Strategic HR
6. Leadership and Management for Managers
7. Fundamentals of Accounting
8. Customer Service Skills for Industrial Equipment
9. Health and Safety - Personal Protective Equipment
10. Effective Communication Skills for Managers

## Batch Processing Strategy

### Week 1: Sales Courses (5 courses)
- Generate 30 pages × 5 courses = 150 pages
- ~2-3 hours per course with AI assistance

### Week 2: Finance Courses (5 courses)
- Focus on accounting and financial management

### Week 3: HR Courses (5 courses)
- Recruitment, performance management, etc.

### Week 4: Supply Chain (5 courses)
- Logistics, procurement, inventory

## Tips for Better Content

1. **Be Specific in Prompts**
   - Include industry context (pumps & valves)
   - Mention target audience (corporate employees)
   - Request specific examples

2. **Iterate**
   - If content is too generic, ask AI to "make it more specific with real examples"
   - Request "add more technical details and data"

3. **Combine Sources**
   - Use ChatGPT for structure
   - Use Perplexity for research/facts
   - Use Claude for refinement

4. **Quality Check**
   - Read generated content
   - Ensure accuracy
   - Add company-specific information

## Quick Update Script

```python
# quick_update.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

async def bulk_update(course_code, pages_dict):
    """
    pages_dict = {
        1: "<html content>",
        2: "<html content>",
        ...
    }
    """
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    course = await db.courses.find_one({"code": course_code})
    module = await db.modules.find_one({"course_id": course['id']})
    
    for page_num, content in pages_dict.items():
        lesson = await db.lessons.find_one({
            "module_id": module['id'],
            "order": page_num - 1
        })
        if lesson:
            await db.lessons.update_one(
                {"id": lesson['id']},
                {"$set": {"content": content}}
            )
            print(f"  ✓ Page {page_num}")
    
    print(f"✅ Updated {len(pages_dict)} pages for {course['title']}")
    client.close()

# Example usage:
# asyncio.run(bulk_update("SALES-001", {1: "<html>...", 2: "<html>..."}))
```

## Time Estimate

- **Per lesson**: 5-10 minutes (with AI)
- **Per course (30 pages)**: 2-3 hours
- **10 priority courses**: 20-30 hours
- **All 93 courses**: 186-279 hours (spread over weeks/months)

## Recommendation

Start with **5-10 high-priority courses** that are most commonly used. Get user feedback, then gradually improve others based on demand.
