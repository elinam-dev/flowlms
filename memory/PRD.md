# Flowitec Go & Grow LMS - Product Requirements Document

## Overview
A professional Learning Management System (LMS) for Flowitec, a corporate engineering company. The system enables learners to enroll in courses, track progress, take quizzes, and earn certificates. Admins can create and manage courses, modules, lessons, and quizzes.

## User Personas

### 1. Admin
- Full access to all system features
- Can create, edit, and delete courses
- Can manage users and assign roles
- Can create modules, lessons, and quizzes
- Can assign courses to users
- Can view analytics and progress reports

### 2. Learner (Engineer/Technician/Corporate Staff)
- Can browse and enroll in published courses
- Can view course content (video, PDF, text)
- Can complete lessons and track progress
- Can take quizzes (multiple choice, true/false, short answer)
- Can earn and download certificates upon course completion

## Core Requirements

### Authentication (Implemented)
- [x] JWT-based authentication
- [x] User registration with employee ID
- [x] Secure login/logout
- [x] Role-based access control (Admin vs Learner)

### Course Management (Implemented)
- [x] Course CRUD operations
- [x] Module creation within courses
- [x] Lesson creation (text, video, PDF, embed)
- [x] Course publishing/draft status
- [x] Course enrollment
- [x] Progress tracking

### Quiz System (Implemented)
- [x] Multiple choice questions
- [x] True/False questions
- [x] Short answer questions
- [x] Passing score configuration
- [x] Quiz submission and scoring

### Certificate System (Implemented)
- [x] Auto-generation on course completion
- [x] PDF download with ReportLab
- [x] Flowitec branding
- [x] Unique certificate numbers

### Admin Dashboard (Implemented)
- [x] Statistics overview
- [x] User management
- [x] Course management
- [x] Progress monitoring

## What's Been Implemented (January 16, 2026)

### Backend (FastAPI + MongoDB)
- Complete REST API with 20+ endpoints
- JWT authentication with role-based access
- Course, Module, Lesson, Quiz CRUD
- Course types: Compulsory, Optional, Assigned
- Progress tracking with auto-calculation
- Certificate generation with ReportLab PDF
- File upload support (video, document, image)
- Daily check-in with streak tracking
- Admin-only user creation (self-registration disabled)

### Frontend (React + Tailwind)
- Flowitec branded UI with professional design
- Login page (no self-registration)
- Welcome back popup on login
- Learner Dashboard with:
  - Daily check-in feature with streak tracking
  - 7-day check-in calendar
  - Colorful gradient stats cards
  - Course progress tracking
- Course Catalog with search and filter
- Course Detail with lesson player
- Quiz component with all question types
- Certificate download
- Admin Dashboard with analytics
- Admin Course Management with course types
- Admin Course Detail (module/lesson/quiz builder)
- Admin User Management with user creation

## Tech Stack
- **Backend**: FastAPI, Python 3.11, Motor (MongoDB async)
- **Database**: MongoDB
- **Frontend**: React 19, Tailwind CSS, Shadcn/UI
- **Auth**: JWT with bcrypt password hashing
- **PDF**: ReportLab

## Prioritized Backlog

### P0 (Critical)
- ✅ Authentication flow
- ✅ Course management
- ✅ Learner enrollment
- ✅ Quiz system
- ✅ Certificate generation

### P1 (High Priority)
- [ ] Add course thumbnails (image upload)
- [ ] Video upload with progress bar
- [ ] Email notifications on enrollment/completion
- [ ] Due dates for assignments

### P2 (Medium Priority)
- [ ] Course analytics dashboard
- [ ] Learner leaderboards
- [ ] Discussion forums per course
- [ ] Course ratings/reviews
- [ ] Batch user import (CSV)

### P3 (Nice to Have)
- [ ] Mobile app (React Native)
- [ ] SCORM compliance
- [ ] Single Sign-On (SSO)
- [ ] Multi-language support
- [ ] Gamification (badges, points)

## Next Tasks
1. Add sample course content with modules and lessons
2. Implement email notifications (SendGrid/Resend)
3. Add course analytics for admins
4. Implement file upload for course thumbnails
5. Add video progress tracking

## Credentials
- **Admin**: admin@flowitec.com / admin123
