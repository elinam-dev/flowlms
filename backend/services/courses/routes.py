from fastapi import APIRouter

courses_router = APIRouter()

@courses_router.get("/")
def get_courses():
    return {"message": "Courses endpoint"}