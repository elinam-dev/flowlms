from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional, Any
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt
import aiofiles
from bson import ObjectId
import mammoth

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Config
JWT_SECRET = os.environ.get('JWT_SECRET', 'flowitec-lms-secret-key-2024')
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Create the main app
app = FastAPI(title="Flowitec Go & Grow LMS")

# Create routers
api_router = APIRouter(prefix="/api")
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
user_router = APIRouter(prefix="/users", tags=["Users"])
course_router = APIRouter(prefix="/courses", tags=["Courses"])
admin_router = APIRouter(prefix="/admin", tags=["Admin"])
progress_router = APIRouter(prefix="/progress", tags=["Progress"])
certificate_router = APIRouter(prefix="/certificates", tags=["Certificates"])
quiz_router = APIRouter(prefix="/quizzes", tags=["Quizzes"])
upload_router = APIRouter(prefix="/upload", tags=["Upload"])

security = HTTPBearer()

# ======================= MODELS =======================

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    employee_id: Optional[str] = None

class UserLogin(BaseModel):
    identifier: str  # Can be email or employee ID
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    employee_id: Optional[str] = None
    role: str
    created_at: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class CourseCreate(BaseModel):
    title: str
    description: str
    thumbnail: Optional[str] = None
    category: Optional[str] = None
    duration_hours: Optional[float] = 0
    is_published: bool = False
    course_type: str = "optional"  # compulsory, optional, assigned

class ModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 0

class LessonCreate(BaseModel):
    title: str
    content_type: str  # video, pdf, text, embed
    content: str  # URL, text content, or embed code
    duration_minutes: Optional[int] = 0
    order: int = 0

class QuizQuestionCreate(BaseModel):
    question: str
    question_type: str  # multiple_choice, true_false, short_answer
    options: Optional[List[str]] = None
    correct_answer: str
    points: int = 1

class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None
    passing_score: int = 70
    questions: List[QuizQuestionCreate]

class QuizSubmission(BaseModel):
    answers: dict  # question_index: answer

class AssignmentCreate(BaseModel):
    title: str
    description: str
    due_date: Optional[str] = None

class ProgressUpdate(BaseModel):
    lesson_id: str
    completed: bool = True

class CourseEnrollment(BaseModel):
    course_id: str

class AdminUserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    employee_id: Optional[str] = None
    role: str = "learner"

class DailyCheckIn(BaseModel):
    date: str

# ======================= HELPERS =======================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await db.users.find_one({"id": user_id}, {"_id": 0, "password": 0})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# ======================= AUTH ROUTES =======================

@auth_router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    # Registration is disabled - only admin can create users
    raise HTTPException(status_code=403, detail="Registration is disabled. Please contact your administrator.")

@auth_router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    # Find user by email or employee ID
    user = await db.users.find_one({
        "$or": [
            {"email": credentials.identifier},
            {"employee_id": credentials.identifier}
        ]
    })
    
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    token = create_token(user["id"], user["role"])
    
    # Return user data without password
    user_data = {
        "id": user["id"],
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "employee_id": user.get("employee_id"),
        "role": user["role"],
        "created_at": user["created_at"]
    }
    
    user_response = UserResponse(**user_data)
    return TokenResponse(access_token=token, user=user_response)

@auth_router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(**current_user)

# ======================= USER ROUTES =======================

@user_router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user

@user_router.put("/profile")
async def update_profile(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    update_data = {}
    if first_name:
        update_data["first_name"] = first_name
    if last_name:
        update_data["last_name"] = last_name
    
    if update_data:
        await db.users.update_one({"id": current_user["id"]}, {"$set": update_data})
    
    updated_user = await db.users.find_one({"id": current_user["id"]}, {"_id": 0, "password": 0})
    return updated_user

@user_router.post("/check-in")
async def daily_check_in(current_user: dict = Depends(get_current_user)):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Get user's check-in history
    user = await db.users.find_one({"id": current_user["id"]})
    check_ins = user.get("check_ins", [])
    last_check_in = user.get("last_check_in")
    streak = user.get("streak", 0)
    
    # Check if already checked in today
    if today in check_ins:
        return {
            "message": "Already checked in today",
            "streak": streak,
            "check_ins": check_ins[-30:],  # Last 30 days
            "already_checked_in": True
        }
    
    # Calculate streak
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    if last_check_in == yesterday:
        streak += 1
    elif last_check_in != today:
        streak = 1  # Reset streak
    
    # Update user
    await db.users.update_one(
        {"id": current_user["id"]},
        {
            "$push": {"check_ins": today},
            "$set": {"last_check_in": today, "streak": streak}
        }
    )
    
    return {
        "message": "Check-in successful!",
        "streak": streak,
        "check_ins": (check_ins + [today])[-30:],
        "already_checked_in": False
    }

@user_router.get("/check-in/status")
async def get_check_in_status(current_user: dict = Depends(get_current_user)):
    user = await db.users.find_one({"id": current_user["id"]}, {"_id": 0})
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    check_ins = user.get("check_ins", [])
    
    return {
        "streak": user.get("streak", 0),
        "check_ins": check_ins[-30:],
        "checked_in_today": today in check_ins,
        "last_check_in": user.get("last_check_in")
    }

# ======================= COURSE ROUTES =======================

@course_router.get("")
@course_router.get("/")
async def get_courses(current_user: dict = Depends(get_current_user)):
    query = {"is_published": True} if current_user["role"] != "admin" else {}
    courses = await db.courses.find(query, {"_id": 0}).to_list(100)
    return courses

@course_router.get("/enrolled")
async def get_enrolled_courses(current_user: dict = Depends(get_current_user)):
    enrolled_ids = current_user.get("enrolled_courses", [])
    if not enrolled_ids:
        return []
    courses = await db.courses.find({"id": {"$in": enrolled_ids}}, {"_id": 0}).to_list(100)
    
    # Add progress info
    for course in courses:
        progress = await db.progress.find_one(
            {"user_id": current_user["id"], "course_id": course["id"]},
            {"_id": 0}
        )
        course["progress"] = progress.get("percentage", 0) if progress else 0
        course["completed_lessons"] = progress.get("completed_lessons", []) if progress else []
    
    return courses

@course_router.get("/{course_id}")
async def get_course(course_id: str, current_user: dict = Depends(get_current_user)):
    course = await db.courses.find_one({"id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Get modules with lessons
    modules = await db.modules.find({"course_id": course_id}, {"_id": 0}).sort("order", 1).to_list(100)
    for module in modules:
        lessons = await db.lessons.find({"module_id": module["id"]}, {"_id": 0}).sort("order", 1).to_list(100)
        module["lessons"] = lessons
        
        # Get quizzes for this module
        quizzes = await db.quizzes.find({"module_id": module["id"]}, {"_id": 0}).to_list(10)
        module["quizzes"] = quizzes
    
    course["modules"] = modules
    
    # Get user progress
    if current_user["id"] in course.get("enrolled_users", []) or current_user["role"] == "admin":
        progress = await db.progress.find_one(
            {"user_id": current_user["id"], "course_id": course_id},
            {"_id": 0}
        )
        course["user_progress"] = progress
    
    return course

@course_router.post("/enroll")
async def enroll_course(enrollment: CourseEnrollment, current_user: dict = Depends(get_current_user)):
    course = await db.courses.find_one({"id": enrollment.course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if already enrolled
    if enrollment.course_id in current_user.get("enrolled_courses", []):
        raise HTTPException(status_code=400, detail="Already enrolled")
    
    # Add to user's enrolled courses
    await db.users.update_one(
        {"id": current_user["id"]},
        {"$push": {"enrolled_courses": enrollment.course_id}}
    )
    
    # Add user to course's enrolled users
    await db.courses.update_one(
        {"id": enrollment.course_id},
        {"$push": {"enrolled_users": current_user["id"]}}
    )
    
    # Initialize progress
    progress_doc = {
        "id": str(uuid.uuid4()),
        "user_id": current_user["id"],
        "course_id": enrollment.course_id,
        "completed_lessons": [],
        "quiz_scores": {},
        "percentage": 0,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "last_accessed": datetime.now(timezone.utc).isoformat()
    }
    await db.progress.insert_one(progress_doc)
    
    return {"message": "Successfully enrolled", "course_id": enrollment.course_id}

# ======================= PROGRESS ROUTES =======================

@progress_router.post("/lesson")
async def update_lesson_progress(progress: ProgressUpdate, current_user: dict = Depends(get_current_user)):
    lesson = await db.lessons.find_one({"id": progress.lesson_id}, {"_id": 0})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    module = await db.modules.find_one({"id": lesson["module_id"]}, {"_id": 0})
    course_id = module["course_id"]
    
    # Update progress
    user_progress = await db.progress.find_one({"user_id": current_user["id"], "course_id": course_id})
    
    if not user_progress:
        raise HTTPException(status_code=400, detail="Not enrolled in this course")
    
    completed_lessons = user_progress.get("completed_lessons", [])
    if progress.completed and progress.lesson_id not in completed_lessons:
        completed_lessons.append(progress.lesson_id)
    elif not progress.completed and progress.lesson_id in completed_lessons:
        completed_lessons.remove(progress.lesson_id)
    
    # Calculate percentage
    total_lessons = await db.lessons.count_documents({"module_id": {"$in": [m["id"] async for m in db.modules.find({"course_id": course_id})]}})
    percentage = (len(completed_lessons) / total_lessons * 100) if total_lessons > 0 else 0
    
    await db.progress.update_one(
        {"user_id": current_user["id"], "course_id": course_id},
        {
            "$set": {
                "completed_lessons": completed_lessons,
                "percentage": round(percentage, 1),
                "last_accessed": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    # Check if course is completed
    if percentage >= 100:
        await check_course_completion(current_user["id"], course_id)
    
    return {"message": "Progress updated", "percentage": round(percentage, 1)}

@progress_router.get("/course/{course_id}")
async def get_course_progress(course_id: str, current_user: dict = Depends(get_current_user)):
    progress = await db.progress.find_one(
        {"user_id": current_user["id"], "course_id": course_id},
        {"_id": 0}
    )
    if not progress:
        return {"percentage": 0, "completed_lessons": [], "quiz_scores": {}}
    return progress

async def check_course_completion(user_id: str, course_id: str):
    progress = await db.progress.find_one({"user_id": user_id, "course_id": course_id})
    if progress and progress.get("percentage", 0) >= 100:
        # Check if all quizzes passed
        quizzes = await db.quizzes.find({"course_id": course_id}).to_list(100)
        quiz_scores = progress.get("quiz_scores", {})
        
        all_passed = True
        for quiz in quizzes:
            score = quiz_scores.get(quiz["id"], {}).get("score", 0)
            if score < quiz.get("passing_score", 70):
                all_passed = False
                break
        
        if all_passed or not quizzes:
            # Mark course as completed
            await db.users.update_one(
                {"id": user_id},
                {"$addToSet": {"completed_courses": course_id}}
            )
            await db.progress.update_one(
                {"user_id": user_id, "course_id": course_id},
                {"$set": {"completed_at": datetime.now(timezone.utc).isoformat()}}
            )
            # Generate certificate
            await generate_certificate(user_id, course_id)

# ======================= QUIZ ROUTES =======================

@quiz_router.get("/{quiz_id}")
async def get_quiz(quiz_id: str, current_user: dict = Depends(get_current_user)):
    quiz = await db.quizzes.find_one({"id": quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Hide correct answers for learners
    if current_user["role"] != "admin":
        for q in quiz.get("questions", []):
            q.pop("correct_answer", None)
    
    return quiz

@quiz_router.post("/{quiz_id}/submit")
async def submit_quiz(quiz_id: str, submission: QuizSubmission, current_user: dict = Depends(get_current_user)):
    quiz = await db.quizzes.find_one({"id": quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Calculate score
    questions = quiz.get("questions", [])
    total_points = sum(q.get("points", 1) for q in questions)
    earned_points = 0
    results = []
    
    for i, question in enumerate(questions):
        user_answer = submission.answers.get(str(i), "")
        correct = user_answer.lower().strip() == question["correct_answer"].lower().strip()
        if correct:
            earned_points += question.get("points", 1)
        results.append({
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": question["correct_answer"],
            "correct": correct
        })
    
    score = (earned_points / total_points * 100) if total_points > 0 else 0
    passed = score >= quiz.get("passing_score", 70)
    
    # Save quiz result
    module = await db.modules.find_one({"id": quiz["module_id"]}, {"_id": 0})
    course_id = module["course_id"] if module else quiz.get("course_id")
    
    await db.progress.update_one(
        {"user_id": current_user["id"], "course_id": course_id},
        {
            "$set": {
                f"quiz_scores.{quiz_id}": {
                    "score": round(score, 1),
                    "passed": passed,
                    "submitted_at": datetime.now(timezone.utc).isoformat()
                }
            }
        }
    )
    
    return {
        "score": round(score, 1),
        "passed": passed,
        "total_points": total_points,
        "earned_points": earned_points,
        "results": results
    }

# ======================= CERTIFICATE ROUTES =======================

async def generate_certificate(user_id: str, course_id: str):
    user = await db.users.find_one({"id": user_id}, {"_id": 0, "password": 0})
    course = await db.courses.find_one({"id": course_id}, {"_id": 0})
    
    if not user or not course:
        return None
    
    cert_id = str(uuid.uuid4())
    certificate = {
        "id": cert_id,
        "user_id": user_id,
        "course_id": course_id,
        "user_name": f"{user['first_name']} {user['last_name']}",
        "course_title": course["title"],
        "issued_at": datetime.now(timezone.utc).isoformat(),
        "certificate_number": f"FGGC-{cert_id[:8].upper()}"
    }
    
    await db.certificates.insert_one(certificate)
    await db.users.update_one(
        {"id": user_id},
        {"$push": {"certificates": cert_id}}
    )
    
    return certificate

@certificate_router.get("/")
async def get_certificates(current_user: dict = Depends(get_current_user)):
    certificates = await db.certificates.find(
        {"user_id": current_user["id"]},
        {"_id": 0}
    ).to_list(100)
    return certificates

@certificate_router.get("/{cert_id}")
async def get_certificate(cert_id: str, current_user: dict = Depends(get_current_user)):
    certificate = await db.certificates.find_one({"id": cert_id}, {"_id": 0})
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    if certificate["user_id"] != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    return certificate

@certificate_router.get("/{cert_id}/pdf")
async def download_certificate_pdf(cert_id: str, current_user: dict = Depends(get_current_user)):
    from fastapi.responses import Response
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import inch
    import io
    
    certificate = await db.certificates.find_one({"id": cert_id}, {"_id": 0})
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    if certificate["user_id"] != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Generate PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    
    # Background
    c.setFillColor(HexColor("#F8FAFC"))
    c.rect(0, 0, width, height, fill=1)
    
    # Border
    c.setStrokeColor(HexColor("#095EB1"))
    c.setLineWidth(4)
    c.rect(30, 30, width - 60, height - 60)
    
    # Inner border
    c.setStrokeColor(HexColor("#0EA5E9"))
    c.setLineWidth(1)
    c.rect(40, 40, width - 80, height - 80)
    
    # Header
    c.setFillColor(HexColor("#095EB1"))
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2, height - 100, "CERTIFICATE OF COMPLETION")
    
    # Company name
    c.setFillColor(HexColor("#0F172A"))
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 150, "Flowitec Go & Grow")
    
    # This certifies text
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#64748B"))
    c.drawCentredString(width / 2, height - 200, "This is to certify that")
    
    # Recipient name
    c.setFillColor(HexColor("#0F172A"))
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height - 250, certificate["user_name"])
    
    # Has completed text
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#64748B"))
    c.drawCentredString(width / 2, height - 290, "has successfully completed the course")
    
    # Course title
    c.setFillColor(HexColor("#095EB1"))
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - 330, certificate["course_title"])
    
    # Date
    issued_date = datetime.fromisoformat(certificate["issued_at"].replace('Z', '+00:00')).strftime("%B %d, %Y")
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#64748B"))
    c.drawCentredString(width / 2, height - 380, f"Issued on {issued_date}")
    
    # Certificate number
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, 60, f"Certificate No: {certificate['certificate_number']}")
    
    c.save()
    buffer.seek(0)
    
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=certificate-{cert_id}.pdf"}
    )

# ======================= ADMIN ROUTES =======================

@admin_router.get("/stats")
async def get_admin_stats(admin: dict = Depends(get_admin_user)):
    total_users = await db.users.count_documents({"role": "learner"})
    total_courses = await db.courses.count_documents({})
    total_enrollments = await db.progress.count_documents({})
    total_certificates = await db.certificates.count_documents({})
    
    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "total_certificates": total_certificates
    }

@admin_router.get("/users")
async def get_all_users(admin: dict = Depends(get_admin_user)):
    users = await db.users.find({}, {"_id": 0, "password": 0}).to_list(1000)
    
    # Enrich users with enrolled course details
    for user in users:
        enrolled_course_ids = user.get("enrolled_courses", [])
        if enrolled_course_ids:
            courses = await db.courses.find(
                {"id": {"$in": enrolled_course_ids}},
                {"_id": 0, "id": 1, "title": 1}
            ).to_list(100)
            user["enrolled_courses_details"] = courses
        else:
            user["enrolled_courses_details"] = []
    
    return users

@admin_router.post("/users")
async def create_user(user_data: AdminUserCreate, admin: dict = Depends(get_admin_user)):
    # Check if email exists
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Get all compulsory courses to auto-enroll the new user
    compulsory_courses = await db.courses.find(
        {"course_type": "compulsory", "is_published": True},
        {"_id": 0, "id": 1}
    ).to_list(100)
    compulsory_course_ids = [c["id"] for c in compulsory_courses]
    
    user_id = str(uuid.uuid4())
    user_doc = {
        "id": user_id,
        "email": user_data.email,
        "password": hash_password(user_data.password),
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "employee_id": user_data.employee_id or f"EMP-{user_id[:8].upper()}",
        "role": user_data.role,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "enrolled_courses": compulsory_course_ids,  # Auto-enroll in compulsory courses
        "completed_courses": [],
        "certificates": [],
        "check_ins": [],
        "streak": 0,
        "last_check_in": None
    }
    
    await db.users.insert_one(user_doc)
    
    # Initialize progress for compulsory courses and add user to course enrolled_users
    for course_id in compulsory_course_ids:
        # Add user to course's enrolled users
        await db.courses.update_one(
            {"id": course_id},
            {"$addToSet": {"enrolled_users": user_id}}
        )
        # Initialize progress
        progress_doc = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "course_id": course_id,
            "completed_lessons": [],
            "quiz_scores": {},
            "percentage": 0,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "last_accessed": datetime.now(timezone.utc).isoformat()
        }
        await db.progress.insert_one(progress_doc)
    
    # Return user without password
    del user_doc["password"]
    user_doc.pop("_id", None)
    return user_doc

@admin_router.delete("/users/{user_id}")
async def delete_user(user_id: str, admin: dict = Depends(get_admin_user)):
    # Don't allow deleting yourself
    if user_id == admin["id"]:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    result = await db.users.delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Clean up user's progress and certificates
    await db.progress.delete_many({"user_id": user_id})
    await db.certificates.delete_many({"user_id": user_id})
    
    return {"message": "User deleted"}

@admin_router.post("/users/{user_id}/role")
async def update_user_role(user_id: str, role: str, admin: dict = Depends(get_admin_user)):
    if role not in ["learner", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    result = await db.users.update_one({"id": user_id}, {"$set": {"role": role}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "Role updated"}

@admin_router.post("/courses")
async def create_course(course: CourseCreate, admin: dict = Depends(get_admin_user)):
    course_id = str(uuid.uuid4())
    course_doc = {
        "id": course_id,
        **course.model_dump(),
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "created_by": admin["id"]
    }
    await db.courses.insert_one(course_doc)
    # Return without MongoDB _id field
    return {
        "id": course_id,
        "title": course.title,
        "description": course.description,
        "thumbnail": course.thumbnail,
        "category": course.category,
        "duration_hours": course.duration_hours,
        "is_published": course.is_published,
        "enrolled_users": [],
        "created_at": course_doc["created_at"],
        "created_by": admin["id"]
    }

@admin_router.put("/courses/{course_id}")
async def update_course(course_id: str, course: CourseCreate, admin: dict = Depends(get_admin_user)):
    result = await db.courses.update_one(
        {"id": course_id},
        {"$set": course.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    
    updated = await db.courses.find_one({"id": course_id}, {"_id": 0})
    return updated

@admin_router.delete("/courses/{course_id}")
async def delete_course(course_id: str, admin: dict = Depends(get_admin_user)):
    # Delete course and related data
    await db.courses.delete_one({"id": course_id})
    await db.modules.delete_many({"course_id": course_id})
    
    # Get all module IDs for this course to delete lessons
    modules = await db.modules.find({"course_id": course_id}).to_list(100)
    module_ids = [m["id"] for m in modules]
    await db.lessons.delete_many({"module_id": {"$in": module_ids}})
    await db.quizzes.delete_many({"module_id": {"$in": module_ids}})
    await db.progress.delete_many({"course_id": course_id})
    
    return {"message": "Course deleted"}

@admin_router.post("/courses/{course_id}/modules")
async def create_module(course_id: str, module: ModuleCreate, admin: dict = Depends(get_admin_user)):
    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    module_id = str(uuid.uuid4())
    module_doc = {
        "id": module_id,
        "course_id": course_id,
        **module.model_dump()
    }
    await db.modules.insert_one(module_doc)
    return {
        "id": module_id,
        "course_id": course_id,
        "title": module.title,
        "description": module.description,
        "order": module.order
    }

@admin_router.put("/modules/{module_id}")
async def update_module(module_id: str, module: ModuleCreate, admin: dict = Depends(get_admin_user)):
    result = await db.modules.update_one(
        {"id": module_id},
        {"$set": module.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Module not found")
    
    updated = await db.modules.find_one({"id": module_id}, {"_id": 0})
    return updated

@admin_router.delete("/modules/{module_id}")
async def delete_module(module_id: str, admin: dict = Depends(get_admin_user)):
    await db.modules.delete_one({"id": module_id})
    await db.lessons.delete_many({"module_id": module_id})
    await db.quizzes.delete_many({"module_id": module_id})
    return {"message": "Module deleted"}

@admin_router.post("/modules/{module_id}/lessons")
async def create_lesson(module_id: str, lesson: LessonCreate, admin: dict = Depends(get_admin_user)):
    module = await db.modules.find_one({"id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    lesson_id = str(uuid.uuid4())
    lesson_doc = {
        "id": lesson_id,
        "module_id": module_id,
        **lesson.model_dump()
    }
    await db.lessons.insert_one(lesson_doc)
    return {
        "id": lesson_id,
        "module_id": module_id,
        "title": lesson.title,
        "content_type": lesson.content_type,
        "content": lesson.content,
        "duration_minutes": lesson.duration_minutes,
        "order": lesson.order
    }

@admin_router.put("/lessons/{lesson_id}")
async def update_lesson(lesson_id: str, lesson: LessonCreate, admin: dict = Depends(get_admin_user)):
    result = await db.lessons.update_one(
        {"id": lesson_id},
        {"$set": lesson.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    updated = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
    return updated

@admin_router.delete("/lessons/{lesson_id}")
async def delete_lesson(lesson_id: str, admin: dict = Depends(get_admin_user)):
    await db.lessons.delete_one({"id": lesson_id})
    return {"message": "Lesson deleted"}

@admin_router.post("/modules/{module_id}/quizzes")
async def create_quiz(module_id: str, quiz: QuizCreate, admin: dict = Depends(get_admin_user)):
    module = await db.modules.find_one({"id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    quiz_id = str(uuid.uuid4())
    quiz_doc = {
        "id": quiz_id,
        "module_id": module_id,
        "course_id": module["course_id"],
        "title": quiz.title,
        "description": quiz.description,
        "passing_score": quiz.passing_score,
        "questions": [q.model_dump() for q in quiz.questions]
    }
    await db.quizzes.insert_one(quiz_doc)
    return {
        "id": quiz_id,
        "module_id": module_id,
        "course_id": module["course_id"],
        "title": quiz.title,
        "description": quiz.description,
        "passing_score": quiz.passing_score,
        "questions": [q.model_dump() for q in quiz.questions]
    }

@admin_router.put("/quizzes/{quiz_id}")
async def update_quiz(quiz_id: str, quiz: QuizCreate, admin: dict = Depends(get_admin_user)):
    result = await db.quizzes.update_one(
        {"id": quiz_id},
        {"$set": {
            "title": quiz.title,
            "description": quiz.description,
            "passing_score": quiz.passing_score,
            "questions": [q.model_dump() for q in quiz.questions]
        }}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    updated = await db.quizzes.find_one({"id": quiz_id}, {"_id": 0})
    return updated

@admin_router.delete("/quizzes/{quiz_id}")
async def delete_quiz(quiz_id: str, admin: dict = Depends(get_admin_user)):
    await db.quizzes.delete_one({"id": quiz_id})
    return {"message": "Quiz deleted"}

@admin_router.post("/courses/{course_id}/assign")
async def assign_course_to_users(course_id: str, user_ids: List[str], admin: dict = Depends(get_admin_user)):
    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    for user_id in user_ids:
        user = await db.users.find_one({"id": user_id})
        if user and course_id not in user.get("enrolled_courses", []):
            await db.users.update_one(
                {"id": user_id},
                {"$push": {"enrolled_courses": course_id}}
            )
            await db.courses.update_one(
                {"id": course_id},
                {"$push": {"enrolled_users": user_id}}
            )
            # Initialize progress
            progress_doc = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "course_id": course_id,
                "completed_lessons": [],
                "quiz_scores": {},
                "percentage": 0,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "last_accessed": datetime.now(timezone.utc).isoformat()
            }
            await db.progress.insert_one(progress_doc)
    
    return {"message": f"Course assigned to {len(user_ids)} users"}

@admin_router.get("/courses/{course_id}/progress")
async def get_course_progress_admin(course_id: str, admin: dict = Depends(get_admin_user)):
    progress_list = await db.progress.find({"course_id": course_id}, {"_id": 0}).to_list(1000)
    
    # Enrich with user info
    for p in progress_list:
        user = await db.users.find_one({"id": p["user_id"]}, {"_id": 0, "password": 0})
        p["user"] = user
    
    return progress_list

# ======================= UPLOAD ROUTES =======================

@upload_router.post("/video")
async def upload_video(
    file: UploadFile = File(...),
    admin: dict = Depends(get_admin_user)
):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")
    
    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    file_path = ROOT_DIR / "uploads" / "videos" / f"{file_id}{file_ext}"
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {"url": f"/api/uploads/videos/{file_id}{file_ext}", "filename": file.filename}

@upload_router.post("/document")
async def upload_document(
    file: UploadFile = File(...),
    admin: dict = Depends(get_admin_user)
):
    allowed_types = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File must be a PDF or Word document")
    
    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    file_path = ROOT_DIR / "uploads" / "documents" / f"{file_id}{file_ext}"
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {"url": f"/api/uploads/documents/{file_id}{file_ext}", "filename": file.filename}

@upload_router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    admin: dict = Depends(get_admin_user)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    file_path = ROOT_DIR / "uploads" / "images" / f"{file_id}{file_ext}"
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {"url": f"/api/uploads/images/{file_id}{file_ext}", "filename": file.filename}

# Document viewer endpoint - converts DOCX to HTML for inline viewing
@upload_router.get("/view/{filename}")
async def view_document(filename: str):
    """View document inline - converts DOCX to HTML, serves PDF as-is"""
    file_path = ROOT_DIR / "uploads" / "documents" / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Handle DOCX files - convert to HTML
    if filename.lower().endswith('.docx'):
        try:
            with open(file_path, 'rb') as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html_content = result.value
                
                # Wrap in a nice styled HTML page
                full_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Document Viewer</title>
                    <style>
                        body {{
                            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                            line-height: 1.6;
                            max-width: 900px;
                            margin: 0 auto;
                            padding: 40px 20px;
                            background: #fff;
                            color: #333;
                        }}
                        h1, h2, h3, h4, h5, h6 {{
                            color: #095EB1;
                            margin-top: 1.5em;
                            margin-bottom: 0.5em;
                        }}
                        h1 {{ font-size: 2em; border-bottom: 2px solid #095EB1; padding-bottom: 0.3em; }}
                        h2 {{ font-size: 1.5em; }}
                        h3 {{ font-size: 1.25em; }}
                        p {{ margin: 1em 0; }}
                        table {{
                            border-collapse: collapse;
                            width: 100%;
                            margin: 1em 0;
                        }}
                        th, td {{
                            border: 1px solid #ddd;
                            padding: 12px;
                            text-align: left;
                        }}
                        th {{
                            background-color: #095EB1;
                            color: white;
                        }}
                        tr:nth-child(even) {{
                            background-color: #f9fafb;
                        }}
                        ul, ol {{
                            margin: 1em 0;
                            padding-left: 2em;
                        }}
                        li {{
                            margin: 0.5em 0;
                        }}
                        strong {{
                            color: #0F172A;
                        }}
                        img {{
                            max-width: 100%;
                            height: auto;
                        }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """
                return HTMLResponse(content=full_html)
        except Exception as e:
            logger.error(f"Error converting DOCX: {e}")
            raise HTTPException(status_code=500, detail="Failed to convert document")
    
    # Handle PDF files - serve with proper headers for embedding
    elif filename.lower().endswith('.pdf'):
        async with aiofiles.open(file_path, 'rb') as f:
            content = await f.read()
        return Response(
            content=content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={filename}",
                "X-Frame-Options": "SAMEORIGIN"
            }
        )
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

# Document serving route
@app.get("/api/uploads/documents/{filename}")
async def serve_document(filename: str):
    try:
        file_path = ROOT_DIR / "uploads" / "documents" / filename
        logger.info(f"Trying to serve document: {file_path}")
        
        if not file_path.exists():
            logger.error(f"Document not found: {file_path}")
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Serve PDF files directly
        if filename.lower().endswith('.pdf'):
            async with aiofiles.open(file_path, 'rb') as f:
                content = await f.read()
            return Response(
                content=content,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"inline; filename={filename}",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "*"
                }
            )
        
        # Serve DOCX files by converting to HTML
        elif filename.lower().endswith('.docx'):
            with open(file_path, 'rb') as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html_content = result.value
                return HTMLResponse(
                    content=html_content,
                    headers={
                        "Access-Control-Allow-Origin": "*"
                    }
                )
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
            
    except Exception as e:
        logger.error(f"Error serving document {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error serving document: {str(e)}")

# ======================= SETUP =======================

# Include routers
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(course_router)
api_router.include_router(admin_router)
api_router.include_router(progress_router)
api_router.include_router(certificate_router)
api_router.include_router(quiz_router)
api_router.include_router(upload_router)

app.include_router(api_router)

# Serve uploaded files
app.mount("/api/uploads", StaticFiles(directory=str(ROOT_DIR / "uploads")), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup():
    # Create admin user if not exists
    admin = await db.users.find_one({"email": "admin@flowitec.com"})
    if not admin:
        admin_doc = {
            "id": str(uuid.uuid4()),
            "email": "admin@flowitec.com",
            "password": hash_password("admin123"),
            "first_name": "Admin",
            "last_name": "User",
            "employee_id": "ADMIN-001",
            "role": "admin",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "enrolled_courses": [],
            "completed_courses": [],
            "certificates": []
        }
        await db.users.insert_one(admin_doc)
        logger.info("Admin user created: admin@flowitec.com / admin123")
    
    # Create test learner user if not exists
    learner = await db.users.find_one({"employee_id": "EMP-TEST-01"})
    if not learner:
        learner_doc = {
            "id": str(uuid.uuid4()),
            "email": "learner@test.com",
            "password": hash_password("learner123"),
            "first_name": "Test",
            "last_name": "Learner",
            "employee_id": "EMP-TEST-01",
            "role": "learner",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "enrolled_courses": [],
            "completed_courses": [],
            "certificates": [],
            "check_ins": [],
            "streak": 0,
            "last_check_in": None
        }
        await db.users.insert_one(learner_doc)
        logger.info("Test learner created: EMP-TEST-01 / learner123")
    
    # Clean up any existing courses first
    await db.courses.delete_many({})
    await db.modules.delete_many({})
    await db.lessons.delete_many({})
    await db.progress.delete_many({})
    
    # Create courses from uploaded documents
    documents = [
        {"file": "Flowitec Code of Ethics & Conduct updated.pdf", "title": "Code of Ethics & Conduct", "category": "Ethics", "type": "compulsory"},
        {"file": "Disciplinary Code.pdf", "title": "Disciplinary Code", "category": "HR Policy", "type": "compulsory"},
        {"file": "Health and Safety Policy 1.docx", "title": "Health & Safety Policy", "category": "Safety", "type": "compulsory"},
        {"file": "Leave Policy -Ghana.pdf", "title": "Leave Policy - Ghana", "category": "HR Policy", "type": "compulsory"},
        {"file": "Leave Policy - Nigeria.docx", "title": "Leave Policy - Nigeria", "category": "HR Policy", "type": "optional"}
    ]
    
    compulsory_course_ids = []
    
    for doc in documents:
        course_id = str(uuid.uuid4())
        course_doc = {
            "id": course_id,
            "title": doc["title"],
            "description": f"Company policy document: {doc['title']}",
            "thumbnail": None,
            "category": doc["category"],
            "duration_hours": 1.0,
            "is_published": True,
            "course_type": doc["type"],
            "enrolled_users": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "created_by": "admin-001"
        }
        await db.courses.insert_one(course_doc)
        
        if doc["type"] == "compulsory":
            compulsory_course_ids.append(course_id)
        
        # Create module
        module_id = str(uuid.uuid4())
        module_doc = {
            "id": module_id,
            "course_id": course_id,
            "title": f"{doc['title']} - Policy Document",
            "description": f"Read and understand the {doc['title']} policy",
            "order": 1
        }
        await db.modules.insert_one(module_doc)
        
        # Create document lesson
        lesson_id = str(uuid.uuid4())
        content_type = "pdf" if doc["file"].endswith(".pdf") else "document"
        lesson_doc = {
            "id": lesson_id,
            "module_id": module_id,
            "title": f"{doc['title']} Document",
            "content_type": content_type,
            "content": f"/api/uploads/documents/{doc['file']}",
            "duration_minutes": 45,
            "order": 1
        }
        await db.lessons.insert_one(lesson_doc)
        
        logger.info(f"Created course: {doc['title']}")
    
    # Auto-enroll all existing users in compulsory courses
    all_users = await db.users.find({"role": "learner"}).to_list(1000)
    for user in all_users:
        await db.users.update_one(
            {"id": user["id"]},
            {"$set": {"enrolled_courses": compulsory_course_ids}}
        )
        
        # Create progress for each compulsory course
        for course_id in compulsory_course_ids:
            await db.courses.update_one(
                {"id": course_id},
                {"$addToSet": {"enrolled_users": user["id"]}}
            )
            
            progress_doc = {
                "id": str(uuid.uuid4()),
                "user_id": user["id"],
                "course_id": course_id,
                "completed_lessons": [],
                "quiz_scores": {},
                "percentage": 0,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "last_accessed": datetime.now(timezone.utc).isoformat()
            }
            await db.progress.insert_one(progress_doc)
    
    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("id", unique=True)
    await db.courses.create_index("id", unique=True)
    await db.modules.create_index("id", unique=True)
    await db.lessons.create_index("id", unique=True)
    await db.quizzes.create_index("id", unique=True)
    await db.progress.create_index([("user_id", 1), ("course_id", 1)])
    await db.certificates.create_index("id", unique=True)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
