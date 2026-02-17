# AI Course Content Generator

This system uses Claude API to generate detailed, professional course content for all courses in the LMS.

## Setup

### 1. Get Claude API Key
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

### 2. Add API Key to .env
Open `backend/.env` and add:
```
CLAUDE_API_KEY=sk-ant-your-api-key-here
```

### 3. Install Required Package
```bash
cd backend
pip install anthropic
```

## Usage

### Generate All Courses
```bash
python generate_courses_with_ai.py
```

### Generate Specific Course
```bash
python generate_courses_with_ai.py SALES-001
```

### Custom Batch Size
```bash
python generate_courses_with_ai.py "" 10
```

## What It Does

For each course:
1. **Generates lesson titles** - Creates contextual, progressive titles
2. **Generates detailed content** - 800-1200 words per lesson with:
   - Specific examples and data
   - Real-world applications
   - Tables, lists, and formatted sections
   - Professional HTML formatting
3. **Generates quiz questions** - 12 questions per course:
   - 6 multiple choice
   - 3 true/false
   - 3 short answer

## Page Counts by Category

- Finance: 60 pages
- Engineering: 58 pages
- Sales: 55 pages
- HR: 52 pages
- Supply Chain: 50 pages
- Management: 48 pages
- Health & Safety: 45 pages
- Personal Development: 40 pages
- Policy: 38 pages
- Language: 35 pages

## Cost Estimate

Using Claude 3.5 Sonnet:
- Input: $3 per million tokens
- Output: $15 per million tokens

Estimated cost per course (50 pages):
- ~$0.50 - $1.50 per course
- Total for 93 courses: ~$50-$150

## Notes

- Processing is done in batches (default: 5 courses at a time)
- Each course takes 5-10 minutes to generate
- Content is unique and contextual to each course
- All existing lessons are replaced with new AI-generated content
- Quizzes are regenerated with course-specific questions

## Troubleshooting

**Error: CLAUDE_API_KEY not found**
- Make sure you added the API key to `.env` file

**Error: anthropic module not found**
- Run: `pip install anthropic`

**API Rate Limits**
- If you hit rate limits, reduce batch size or add delays

**Content Quality**
- Review generated content before deploying
- You can regenerate specific courses if needed
