import React from 'react';

const ReadMe = () => {
  return (
    <div className="min-h-screen bg-[#F8FAFC] p-6">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-sm p-8">
        <div className="prose prose-slate max-w-none">
          <h1 className="text-3xl font-bold text-[#095EB1] mb-6">Flowitec Go & Grow LMS</h1>
          <p className="text-lg text-slate-600 mb-8">A professional Learning Management System for corporate training.</p>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-slate-800 mb-4">Tech Stack</h2>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Frontend:</strong> React 19, Tailwind CSS, Shadcn/UI</li>
              <li><strong>Backend:</strong> FastAPI (Python)</li>
              <li><strong>Database:</strong> MongoDB</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-slate-800 mb-4">Features</h2>
            <ul className="list-disc pl-6 space-y-2">
              <li>JWT Authentication (Email or Employee ID login)</li>
              <li>Course Management (Compulsory, Optional, Assigned)</li>
              <li>Module & Lesson Builder</li>
              <li>Quiz System (Multiple Choice, True/False, Short Answer)</li>
              <li>Progress Tracking</li>
              <li>Daily Check-in with Streak</li>
              <li>PDF Certificate Generation</li>
              <li>Admin Dashboard</li>
              <li>User Management (Admin-only creation)</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-slate-800 mb-4">Demo Credentials</h2>
            <div className="bg-slate-50 p-4 rounded-lg">
              <p><strong>Admin:</strong> admin@flowitec.com / admin123</p>
              <p><strong>Learner:</strong> EMP-TEST-01 / learner123</p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-slate-800 mb-4">Environment Variables</h2>
            
            <h3 className="text-xl font-medium text-slate-700 mb-3">Backend (.env)</h3>
            <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto mb-4">
{`MONGO_URL=mongodb://localhost:27017
DB_NAME=flowitec_lms
JWT_SECRET=your-secret-key-here
CORS_ORIGINS=http://localhost:3000`}
            </pre>

            <h3 className="text-xl font-medium text-slate-700 mb-3">Frontend (.env)</h3>
            <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto">
{`REACT_APP_BACKEND_URL=http://localhost:8000`}
            </pre>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-slate-800 mb-4">Local Development Setup</h2>
            
            <h3 className="text-xl font-medium text-slate-700 mb-3">Prerequisites</h3>
            <ul className="list-disc pl-6 space-y-1 mb-4">
              <li>Node.js 18+</li>
              <li>Python 3.11+</li>
              <li>MongoDB (local or MongoDB Atlas)</li>
            </ul>

            <h3 className="text-xl font-medium text-slate-700 mb-3">Backend Setup</h3>
            <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto mb-4">
{`cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB connection string

# Run backend
uvicorn server:app --host 0.0.0.0 --port 8000 --reload`}
            </pre>

            <h3 className="text-xl font-medium text-slate-700 mb-3">Frontend Setup</h3>
            <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto mb-4">
{`cd frontend

# Install dependencies
yarn install

# Create .env file
cp .env.example .env
# Edit .env with your backend URL

# Run frontend
yarn start`}
            </pre>

            <h3 className="text-xl font-medium text-slate-700 mb-3">Access the Application</h3>
            <ul className="list-disc pl-6 space-y-1">
              <li>Frontend: <a href="http://localhost:3000" className="text-[#095EB1] hover:underline">http://localhost:3000</a></li>
              <li>Backend API: <a href="http://localhost:8000/api" className="text-[#095EB1] hover:underline">http://localhost:8000/api</a></li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-slate-800 mb-4">License</h2>
            <p className="text-slate-600">Proprietary - Flowitec</p>
          </section>
        </div>
      </div>
    </div>
  );
};

export default ReadMe;