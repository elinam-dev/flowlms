@echo off
cd backend
echo Starting backend server...
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
