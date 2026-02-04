# Flowitec Go & Grow LMS - Product Requirements Document

## Overview
Corporate Learning Management System (LMS) with Alison.com-style modern UI/UX design featuring page-based course navigation and Career Beetle succession planning.

## Original Problem Statement
1. Redesign LMS to look like Alison.com with horizontal scrolling and page-based course viewing
2. Delete all existing courses and replace with 4 Flowitec policy courses
3. Create Career Beetle feature based on succession plan Excel data

## User Choices
- Keep Flowitec blue (#095EB1) branding
- Page-by-page course navigation (not scroll) with Next/Previous buttons
- Progress tracked per page
- Career Beetle with 5 departments from Excel data

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
- **Frontend**: React.js + Tailwind CSS + shadcn/ui
- **Backend**: FastAPI (Python)
- **Database**: MongoDB

## What's Been Implemented (Feb 4, 2026)

### Phase 1: Alison.com Style Redesign ✅
- Horizontal scrolling course carousels
- Course cards with hover overlays
- Category tabs (All, Popular, Required, Optional, My Courses)
- Hero sections with search

### Phase 2: New Courses & Page-Based Navigation ✅
1. **4 New Policy Courses Created**:
   - Leave Policy - Ghana (6 pages)
   - Code of Ethics & Conduct (7 pages)
   - Disciplinary Code (4 pages)
   - Health & Safety Policy (6 pages)

2. **Page-Based Course Viewer**:
   - Next/Previous button navigation
   - Page dots for visual progress
   - "Complete & Continue" button per page
   - Progress bar updates as pages complete
   - Styled policy content with highlight boxes

3. **Course Detail Redesign**:
   - "What You'll Learn" section before enrollment
   - Page count display
   - Start Course enrollment button

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

3. **Navigation Integration**:
   - Career Beetle in main nav menu
   - Department tab switching
   - CTA "Start Learning" button

## Files Created/Updated
- `/app/seed_courses.py` - Database seeding script
- `/app/frontend/src/pages/learner/CourseDetail.js` - Page-based viewer
- `/app/frontend/src/pages/learner/CareerBeetle.js` - Career progression
- `/app/frontend/src/components/layout/Navbar.js` - Navigation update
- `/app/frontend/src/App.js` - Routes update
- `/app/backend/server.py` - Career Beetle API endpoints

## Prioritized Backlog

### P0 (Completed) ✅
- Page-based course navigation
- Career Beetle with all 5 departments
- 4 policy courses with formatted content

### P1 (Important)
- [ ] Course completion certificate for policy courses
- [ ] Admin ability to edit/add Career Beetle roles
- [ ] Mobile responsive Career Beetle

### P2 (Nice to Have)
- [ ] Quiz at end of each course
- [ ] Career path recommendation based on current role
- [ ] PDF export of Career Beetle progression

## Next Tasks
1. Add quizzes to policy courses
2. Certificate generation after course completion
3. Career path recommendation algorithm
4. Admin dashboard for Career Beetle management
