#!/bin/bash

# Flowitec Go & Grow LMS - Local Setup Script

echo "🚀 Setting up Flowitec Go & Grow LMS..."

# Check for required tools
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }
command -v yarn >/dev/null 2>&1 || { echo "❌ Yarn is required but not installed. Run: npm install -g yarn"; exit 1; }

# Backend setup
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt --quiet

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Created backend/.env - Please update with your MongoDB connection string"
fi

cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
yarn install --silent

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Created frontend/.env"
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "1. Start MongoDB (if running locally)"
echo ""
echo "2. Start Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
echo ""
echo "3. Start Frontend (in a new terminal):"
echo "   cd frontend"
echo "   yarn start"
echo ""
echo "4. Open http://localhost:3000"
echo ""
echo "Demo credentials:"
echo "   Admin: admin@flowitec.com / admin123"
echo "   Learner: EMP-TEST-01 / learner123"
