from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.get("/login")
def login():
    return {"message": "Login endpoint"}

@auth_router.get("/register")
def register():
    return {"message": "Register endpoint"}