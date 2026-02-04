# Flowitec Go & Grow LMS - Product Requirements Document

## Overview
Corporate Learning Management System (LMS) with Alison.com-style modern UI/UX redesign.

## Original Problem Statement
Redesign the LMS to look more like Alison.com in terms of:
- Scrolling behavior
- Course display (horizontal carousels)
- Course card interactions (hover overlays)
- Course detail page layout

## User Choices
- Keep Flowitec blue (#095EB1) branding
- All pages redesigned: Dashboard, Courses, Course Detail, Certificates, Profile
- Full Alison-style features: carousels, tabs, hover overlays, "You Will Learn" section

## User Personas
1. **Learner** - Corporate employees seeking training and certifications
2. **Admin** - Administrators managing courses, users, and content

## Core Requirements (Static)
- User authentication (Employee ID or Email login)
- Course catalog with categories
- Course enrollment and progress tracking
- Video/Document content support
- Quiz assessments
- Certificate generation
- Daily check-in with streaks
- Admin course management

## Architecture
- **Frontend**: React.js + Tailwind CSS + shadcn/ui components
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **File Storage**: Local uploads directory

## What's Been Implemented (Feb 4, 2026)

### Alison.com Style Redesign ✅
1. **New Components Created**
   - `CourseCard.js` - Course cards with hover overlay showing "More Info" and "Start Learning" buttons
   - `CourseCarousel.js` - Horizontal scrolling carousel using Embla Carousel

2. **Courses Page Redesign**
   - Large hero section with search bar
   - Category tabs (All Courses, Popular, Required, Optional, My Courses)
   - Category filter dropdown
   - Horizontal scrolling course carousels with navigation arrows
   - Course cards with progress bars, badges, and stats

3. **Course Detail Page Redesign**
   - Breadcrumb navigation
   - "What You Will Learn" section with learning outcomes
   - Course stats row (duration, learners, lessons, modules)
   - Sidebar enrollment card with progress circle
   - Tabs: Overview and Course Content
   - Course curriculum with collapsible modules

4. **Dashboard Page Redesign**
   - Personalized greeting with time-based salutation
   - Daily Check-in card with streak counter
   - Last 7 Days check-in calendar
   - Colorful gradient stat cards (Enrolled, In Progress, Completed, Certificates)
   - Continue Learning carousel
   - Recommended For You carousel

5. **CSS Enhancements**
   - Smooth scrolling animations
   - Hero pattern backgrounds
   - Glass morphism effects
   - Staggered fade-up animations
   - Tab indicator animations
   - Course card lift hover effect

### Technical Fixes
- Added proxy configuration in craco.config.js for API routing
- Disabled visual-edits middleware to fix body parsing issues with proxy
- Created necessary upload directories

## Prioritized Backlog

### P0 (Critical)
- ✅ Alison-style horizontal carousels
- ✅ Course card hover overlays
- ✅ Course detail "You Will Learn" section
- ✅ Category tabs and filtering

### P1 (Important)
- [ ] Admin dashboard redesign to match Alison style
- [ ] Certificate viewer enhancement
- [ ] Mobile responsive improvements

### P2 (Nice to Have)
- [ ] Course search with autocomplete
- [ ] Course recommendations based on history
- [ ] Social sharing features
- [ ] Course reviews/ratings

## Next Tasks
1. Test all pages on mobile viewports
2. Add more course content/seed data
3. Enhance certificate download experience
4. Add course completion celebrations/animations
