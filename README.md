# Flowitec Go & Grow LMS

A professional Learning Management System for corporate training.

## Tech Stack
- **Frontend**: React 19, Tailwind CSS, Shadcn/UI
- **Backend**: FastAPI (Python)
- **Database**: MongoDB

## Local Development Setup

### Prerequisites
- Node.js 18+ 
- Python 3.11+
- MongoDB (local or MongoDB Atlas)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB connection string

# Run backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
yarn install

# Create .env file
cp .env.example .env
# Edit .env with your backend URL

# Run frontend
yarn start
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001/api

## Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=flowitec_lms
JWT_SECRET=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

## Demo Credentials
- **Admin**: admin@flowitec.com / admin123
- **Learner**: EMP-TEST-01 / learner123

## Vercel Deployment

### Frontend Deployment
1. Push code to GitHub
2. Import project in Vercel
3. Set root directory to `frontend`
4. Add environment variable:
   - `REACT_APP_BACKEND_URL` = your backend URL

### Backend Deployment
For the FastAPI backend, you can use:
- **Railway.app** (recommended for Python)
- **Render.com**
- **Fly.io**

## Features
- JWT Authentication (Email or Employee ID login)
- Course Management (Compulsory, Optional, Assigned)
- Module & Lesson Builder
- Quiz System (Multiple Choice, True/False, Short Answer)
- Progress Tracking
- Daily Check-in with Streak
- PDF Certificate Generation
- Admin Dashboard
- User Management (Admin-only creation)

## License
Proprietary - Flowitec
