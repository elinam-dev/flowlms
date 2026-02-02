import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auth.routes import auth_router
from services.courses.routes import courses_router
from services.users.routes import users_router

from fastapi import FastAPI

app = FastAPI()

# Include routers for modular services
app.include_router(auth_router, prefix="/auth")
app.include_router(courses_router, prefix="/courses")
app.include_router(users_router, prefix="/users")

@app.get("/")
def read_root():
    return {"message": "Welcome to the modular backend!"}