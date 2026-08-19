#!/bin/bash
set -e

# Flowitec Go & Grow LMS - Start Script
#
# This script starts the backend (Python / FastAPI) service. Railpack
# builds this project using the root Procfile, which defines separate
# process types for the backend and frontend services. This script is
# kept for local/manual use and simply boots the backend API.

echo "🚀 Starting Flowitec Go & Grow LMS backend..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# Backend (Python / FastAPI)
# ---------------------------------------------------------------------------
cd "$ROOT_DIR/backend"

echo "▶️  Starting backend..."
exec python3 -m uvicorn server:app --host 0.0.0.0 --port "${PORT:-8001}"
