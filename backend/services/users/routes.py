from fastapi import APIRouter

users_router = APIRouter()

@users_router.get("/")
def get_users():
    return {"message": "Users endpoint"}