from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from bson import ObjectId
import os

courses_router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads", "documents")

@courses_router.get("/")
def get_courses():
    return {"message": "Courses endpoint"}

@courses_router.get("/documents/{document_id}")
async def get_course_document(document_id: str):
    # Import db from the main server module
    import sys
    sys.path.append('..')
    from server import db

    # Find document by id OR _id
    document = await db.documents.find_one({
        "$or": [
            {"id": document_id},
            {"_id": ObjectId(document_id)} if ObjectId.is_valid(document_id) else {}
        ]
    })

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_name = document.get("file_name")
    if not file_name:
        raise HTTPException(status_code=404, detail="File name missing")

    file_path = os.path.join(UPLOADS_DIR, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=file_name
    )