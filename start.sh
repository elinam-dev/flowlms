#!/bin/bash
set -e

# Flowitec Go & Grow LMS - Start Script
#
# This script installs dependencies for both the backend and frontend
# services and starts them concurrently. It exists so that Railpack has
# a clear entry point for building and running this monorepo.

echo "🚀 Starting Flowitec Go & Grow LMS..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# Backend (Python / FastAPI)
# ---------------------------------------------------------------------------
echo "📦 Installing backend dependencies..."
cd "$ROOT_DIR/backend"
python3 -m pip install --no-cache-dir -r requirements.txt

echo "▶️  Starting backend..."
python3 -m uvicorn server:app --host 0.0.0.0 --port "${PORT:-8001}" &
BACKEND_PID=$!

# ---------------------------------------------------------------------------
# Frontend (React)
# ---------------------------------------------------------------------------
echo "📦 Installing frontend dependencies..."
cd "$ROOT_DIR/frontend"
if command -v yarn >/dev/null 2>&1; then
    yarn install --frozen-lockfile || yarn install
else
    npm install
fi

echo "▶️  Starting frontend..."
if command -v yarn >/dev/null 2>&1; then
    yarn start &
else
    npm start &
fi
FRONTEND_PID=$!

# ---------------------------------------------------------------------------
# Keep the process alive and forward termination signals
# ---------------------------------------------------------------------------
trap 'kill $BACKEND_PID $FRONTEND_PID 2>/dev/null' SIGINT SIGTERM

wait $BACKEND_PID $FRONTEND_PID
