# Flowitec Go & Grow LMS - Product Requirements Document

## Overview
Corporate Learning Management System (LMS) with Alison.com-style modern UI/UX design featuring page-based course navigation and Career Beetle succession planning.

## Original Problem Statement
1. Redesign LMS to look like Alison.com with horizontal scrolling and page-based course viewing
2. Create Career Beetle feature based on succession plan Excel data
3. Create comprehensive SALES (ENGINEER) courses for Flowitec (pumps & valves company)

## User Choices
- Keep Flowitec blue (#095EB1) branding
- Page-by-page course navigation (not scroll) with Next/Previous buttons
- Progress tracked per page
- Career Beetle with 5 departments from Excel data
- Course categories: SALES (ENGINEER), HR, FINANCE, SUPPLY CHAIN, LANGUAGES (FRENCH)

## User Personas
1. **Learner** - Corporate employees completing required training
2. **Admin** - Administrators managing courses and users

## Core Requirements (Static)
- User authentication (Employee ID or Email)
- Course catalog with horizontal carousels
- Page-based course content viewer
- Progress tracking per page
- Certificate generation
- Career Beetle succession planning

## Architecture
- **Frontend**: React.js + Tailwind CSS + shadcn/ui + Embla Carousel
- **Backend**: FastAPI (Python)
- **Database**: MongoDB

## What's Been Implemented (Feb 9, 2026)

### Phase 1: Alison.com Style Redesign ✅
- Horizontal scrolling course carousels
- Course cards with hover overlays (More Info, Start Learning buttons)
- Category tabs (All, Popular, Required, Optional, My Courses)
- Hero sections with search

### Phase 2: Page-Based Navigation ✅
- Next/Previous button navigation
- Page dots for visual progress
- "Complete & Continue" button per page
- Progress bar updates as pages complete
- Styled content with tables, highlight boxes, info boxes

### Phase 3: Career Beetle Feature ✅
1. **5 Departments**:
   - Sales (8 roles)
   - Supply Chain (6 roles)
   - Finance (5 roles)
   - Human Resource (5 roles)
   - Facilities (5 roles)

2. **Career Ladder Visualization**:
   - Vertical progression line
   - Level badges (Entry → Senior Level)
   - Expandable role cards
   - Key Skills, Qualifications, Timeline

### Phase 4: 17 SALES (ENGINEER) Courses ✅ (Feb 9, 2026)
All 17 courses created with comprehensive content tailored to Flowitec (pumps & valves):

| Code | Course Title | Duration |
|------|-------------|----------|
| SE-CS-001 | Customer Service Skills for Industrial Equipment | 15h |
| SE-CSM-002 | B2B Customer Success Management | 12h |
| SE-TEL-003 | Customer Care Skills and Telephone Etiquette | 10h |
| SE-DSM-004 | Diploma in Sales Management | 20h |
| SE-BPD-005 | B2B Partnership Development | 12h |
| SE-MIN-006 | Mastering Influence and Negotiation | 14h |
| SE-MMI-007 | Marketing Management - Capturing Market Insights | 12h |
| SE-IMM-008 | Introduction to Marketing Management | 10h |
| SE-MIS-009 | Mastering Influence in Sales | 12h |
| SE-STI-010 | Sales Techniques - Interacting with Customers | 12h |
| SE-SNS-011 | Sales and Negotiation Skills | 14h |
| SE-KAM-012 | Understanding Key Account Management | 14h |
| SE-MBC-013 | Understanding Market Demand, Branding and Communications | 12h |
| SE-ESS-014 | Effective Sales Skills | 12h |
| SE-CSS-015 | Sales Techniques - Using Competitive Strategies | 12h |
| SE-BLG-016 | B2B Lead Generation Techniques | 10h |
| SE-ABM-017 | Advanced B2B Marketing Strategies | 14h |

**Course Content Features:**
- Each course has 4-16 pages/lessons
- Content reframed for Flowitec's pumps, valves, and fluid control business
- Comprehensive modules covering:
  - Technical knowledge (pump types, valve types, applications)
  - Customer service skills
  - Communication best practices
  - Sales techniques
  - Complaint handling
  - Stress management
- Industry-specific examples (Mining, Water Treatment, Manufacturing, Agriculture)
- Practical applications with Flowitec products

## Files Created/Modified

### Backend
- `/app/backend/seed_sales_courses_full.py` - Comprehensive seeding script for 17 courses
- `/app/backend/server.py` - Added admin endpoint for course seeding

### Frontend
- `/app/frontend/src/pages/learner/CourseDetail.js` - Page-based viewer
- `/app/frontend/src/pages/learner/CareerBeetle.js` - Career progression
- `/app/frontend/src/components/CourseCard.js` - Alison-style course cards
- `/app/frontend/src/components/CourseCarousel.js` - Horizontal carousels
- `/app/frontend/src/components/layout/Navbar.js` - Navigation with Career Beetle

## Prioritized Backlog

### P0 (Completed) ✅
- Page-based course navigation
- Career Beetle with all 5 departments
- 17 SALES (ENGINEER) courses

### P1 (High Priority) - Next Tasks
- [ ] Create HR category courses (links needed from user)
- [ ] Create FINANCE category courses (links needed from user)
- [ ] Create SUPPLY CHAIN category courses (links needed from user)
- [ ] Create LANGUAGES (FRENCH) category courses (links needed from user)
- [ ] Course completion certificates

### P2 (Medium Priority)
- [ ] Quizzes at end of each course
- [ ] Admin ability to edit/add Career Beetle roles
- [ ] Mobile responsive improvements

### P3 (Nice to Have)
- [ ] Career path recommendation based on current role
- [ ] PDF export of Career Beetle progression
- [ ] Advanced analytics dashboard

## API Endpoints

### Courses
- `GET /api/courses/` - List all courses
- `GET /api/courses/{id}` - Get course details
- `POST /api/courses/enroll` - Enroll user in course
- `POST /api/courses/progress` - Update lesson progress

### Career Beetle
- `GET /api/career-beetle/` - Get all career path data

### Admin
- `POST /api/admin/seed-sales-courses` - Seed 17 SALES courses (WARNING: deletes existing)

## Test Credentials
- **Learner**: EMP-TEST-01 / learner123
- **Admin**: admin / admin123
