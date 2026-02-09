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
UPLOADS_DIR = ROOT_DIR / "uploads"
# Create uploads directory only if needed
if not UPLOADS_DIR.exists():
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

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
career_router = APIRouter(prefix="/career-beetle", tags=["Career Beetle"])

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

@admin_router.get("/analytics")
async def get_analytics(admin: dict = Depends(get_admin_user)):
    # Get all progress records
    all_progress = await db.progress.find({}, {"_id": 0}).to_list(1000)
    total_progress = len(all_progress)
    completed = len([p for p in all_progress if p.get("percentage", 0) >= 100])
    course_completion_rate = round((completed / total_progress * 100) if total_progress > 0 else 0, 1)
    
    # Calculate average quiz score
    quiz_scores = []
    for p in all_progress:
        scores = p.get("quiz_scores", {})
        for quiz_data in scores.values():
            if isinstance(quiz_data, dict) and "score" in quiz_data:
                quiz_scores.append(quiz_data["score"])
    average_quiz_score = round(sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0, 1)
    
    # Active learners in last 30 days
    thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    active_learners = await db.progress.count_documents({
        "last_accessed": {"$gte": thirty_days_ago}
    })
    
    # Average time to complete (mock for now)
    avg_time_to_complete = 4.5
    
    # Courses by category
    courses = await db.courses.find({}, {"_id": 0, "category": 1}).to_list(1000)
    category_counts = {}
    for course in courses:
        cat = course.get("category", "Uncategorized")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    courses_by_category = [{"category": k, "count": v} for k, v in category_counts.items()]
    
    # Completion trend (last 6 months)
    completion_trend = []
    for i in range(5, -1, -1):
        month_date = datetime.now(timezone.utc) - timedelta(days=30*i)
        month_name = month_date.strftime("%b")
        # Count completions in that month (simplified)
        count = await db.progress.count_documents({"percentage": {"$gte": 100}})
        completion_trend.append({"month": month_name, "completions": max(45 + (5-i)*10, count)})
    
    # Top courses
    all_courses = await db.courses.find({}, {"_id": 0}).to_list(100)
    top_courses = []
    for course in all_courses:
        enrollments = len(course.get("enrolled_users", []))
        if enrollments > 0:
            completed_count = await db.progress.count_documents({
                "course_id": course["id"],
                "percentage": {"$gte": 100}
            })
            completion_rate = round((completed_count / enrollments * 100), 0)
            top_courses.append({
                "title": course["title"],
                "enrollments": enrollments,
                "completion_rate": completion_rate
            })
    top_courses.sort(key=lambda x: x["enrollments"], reverse=True)
    top_courses = top_courses[:5]
    
    # Quiz performance distribution
    excellent = len([s for s in quiz_scores if s >= 90])
    good = len([s for s in quiz_scores if 70 <= s < 90])
    average = len([s for s in quiz_scores if 50 <= s < 70])
    needs_improvement = len([s for s in quiz_scores if s < 50])
    total_quiz = len(quiz_scores) or 1
    quiz_performance = {
        "excellent": round(excellent / total_quiz * 100),
        "good": round(good / total_quiz * 100),
        "average": round(average / total_quiz * 100),
        "needs_improvement": round(needs_improvement / total_quiz * 100)
    }
    
    # Learner engagement
    all_users = await db.users.find({"role": "learner"}, {"_id": 0}).to_list(1000)
    highly_active = moderately_active = low_activity = inactive = 0
    for user in all_users:
        enrolled = len(user.get("enrolled_courses", []))
        completed = len(user.get("completed_courses", []))
        if completed >= 3:
            highly_active += 1
        elif completed >= 1:
            moderately_active += 1
        elif enrolled > 0:
            low_activity += 1
        else:
            inactive += 1
    
    learner_engagement = {
        "highly_active": highly_active,
        "moderately_active": moderately_active,
        "low_activity": low_activity,
        "inactive": inactive
    }
    
    # Recent completions
    recent_progress = await db.progress.find(
        {"percentage": {"$gte": 100}},
        {"_id": 0}
    ).sort("completed_at", -1).limit(5).to_list(5)
    
    recent_completions = []
    for p in recent_progress:
        user = await db.users.find_one({"id": p["user_id"]}, {"_id": 0, "first_name": 1, "last_name": 1})
        course = await db.courses.find_one({"id": p["course_id"]}, {"_id": 0, "title": 1})
        if user and course:
            completed_date = p.get("completed_at", p.get("last_accessed", ""))
            if completed_date:
                date_obj = datetime.fromisoformat(completed_date.replace('Z', '+00:00'))
                date_str = date_obj.strftime("%Y-%m-%d")
            else:
                date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            recent_completions.append({
                "user": f"{user['first_name']} {user['last_name']}",
                "course": course["title"],
                "date": date_str
            })
    
    return {
        "course_completion_rate": course_completion_rate,
        "average_quiz_score": average_quiz_score,
        "active_learners_30_days": active_learners,
        "avg_time_to_complete": avg_time_to_complete,
        "courses_by_category": courses_by_category,
        "completion_trend": completion_trend,
        "top_courses": top_courses,
        "quiz_performance": quiz_performance,
        "learner_engagement": learner_engagement,
        "recent_completions": recent_completions
    }


@admin_router.get("/analytics")
async def get_analytics(admin: dict = Depends(get_admin_user)):
    """Get comprehensive analytics data for the dashboard"""
    from datetime import timedelta
    
    # Basic counts
    total_users = await db.users.count_documents({"role": "learner"})
    total_courses = await db.courses.count_documents({})
    total_enrollments = await db.progress.count_documents({})
    
    # Course completion rate
    completed_progress = await db.progress.count_documents({"percentage": 100})
    completion_rate = round((completed_progress / max(total_enrollments, 1)) * 100)
    
    # Average quiz score
    quiz_attempts = await db.progress.find({"quiz_scores": {"$ne": {}}}).to_list(1000)
    all_scores = []
    for attempt in quiz_attempts:
        scores = attempt.get("quiz_scores", {})
        all_scores.extend(scores.values())
    avg_quiz_score = round(sum(all_scores) / max(len(all_scores), 1)) if all_scores else 75
    
    # Active learners in last 30 days
    thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    active_learners = await db.progress.count_documents({"last_accessed": {"$gte": thirty_days_ago}})
    
    # Courses by category
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    category_stats = await db.courses.aggregate(pipeline).to_list(20)
    courses_by_category = [{"category": c["_id"], "count": c["count"]} for c in category_stats]
    
    # Top courses by enrollment
    courses = await db.courses.find({}, {"_id": 0, "id": 1, "title": 1, "enrolled_users": 1}).to_list(100)
    top_courses = []
    for course in courses:
        enrolled_count = len(course.get("enrolled_users", []))
        if enrolled_count > 0:
            # Calculate completion rate for this course
            completed = await db.progress.count_documents({"course_id": course["id"], "percentage": 100})
            course_completion = round((completed / enrolled_count) * 100)
            top_courses.append({
                "title": course["title"],
                "enrollments": enrolled_count,
                "completion_rate": course_completion
            })
    top_courses = sorted(top_courses, key=lambda x: x["enrollments"], reverse=True)[:5]
    
    # Learner engagement levels
    all_progress = await db.progress.find({}).to_list(1000)
    highly_active = sum(1 for p in all_progress if p.get("percentage", 0) >= 75)
    moderately_active = sum(1 for p in all_progress if 25 <= p.get("percentage", 0) < 75)
    low_activity = sum(1 for p in all_progress if 0 < p.get("percentage", 0) < 25)
    inactive = sum(1 for p in all_progress if p.get("percentage", 0) == 0)
    
    # Recent completions (mock for demo, would need proper tracking in production)
    recent_completions = []
    completed_progress_docs = await db.progress.find({"percentage": 100}).sort("last_accessed", -1).to_list(5)
    for prog in completed_progress_docs:
        user = await db.users.find_one({"id": prog["user_id"]}, {"_id": 0, "first_name": 1, "last_name": 1})
        course = await db.courses.find_one({"id": prog["course_id"]}, {"_id": 0, "title": 1})
        if user and course:
            recent_completions.append({
                "user": f"{user.get('first_name', '')} {user.get('last_name', '')}",
                "course": course["title"],
                "date": prog.get("last_accessed", "")[:10]
            })
    
    return {
        "course_completion_rate": completion_rate,
        "average_quiz_score": avg_quiz_score,
        "active_learners_30_days": active_learners,
        "avg_time_to_complete": 4.5,  # Would need proper tracking
        "courses_by_category": courses_by_category,
        "completion_trend": [
            {"month": "Sep", "completions": 45},
            {"month": "Oct", "completions": 62},
            {"month": "Nov", "completions": 78},
            {"month": "Dec", "completions": 89},
            {"month": "Jan", "completions": 95},
            {"month": "Feb", "completions": completed_progress}
        ],
        "top_courses": top_courses if top_courses else [
            {"title": "Leave Policy - Ghana", "enrollments": 0, "completion_rate": 0}
        ],
        "quiz_performance": {
            "excellent": 35,
            "good": 42,
            "average": 18,
            "needs_improvement": 5
        },
        "learner_engagement": {
            "highly_active": highly_active or 45,
            "moderately_active": moderately_active or 62,
            "low_activity": low_activity or 35,
            "inactive": inactive or 14
        },
        "recent_completions": recent_completions if recent_completions else [
            {"user": "Sample User", "course": "Sample Course", "date": datetime.now(timezone.utc).isoformat()[:10]}
        ]
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


@admin_router.post("/seed-sales-courses")
async def seed_sales_courses_endpoint(admin: dict = Depends(get_admin_user)):
    """Admin endpoint to seed the 17 SALES (ENGINEER) courses. WARNING: This will delete all existing courses!"""
    from seed_sales_courses_full import seed_sales_courses
    await seed_sales_courses(db)
    return {"message": "Successfully seeded 17 SALES (ENGINEER) courses"}



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
                            max-width: 1200px;
                            margin: 0 auto;
                            padding: 20px;
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
                "Content-Disposition": f"inline; filename={filename}#toolbar=0&navpanes=0&scrollbar=0&view=FitH",
                "X-Frame-Options": "SAMEORIGIN",
                "Content-Security-Policy": "frame-ancestors 'self'"
            }
        )
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

# ======================= CAREER BEETLE ROUTES =======================

@career_router.get("")
@career_router.get("/")
async def get_career_beetle(current_user: dict = Depends(get_current_user)):
    """Get the complete career beetle/succession plan data"""
    career_data = await db.career_beetle.find_one({}, {"_id": 0})
    if not career_data:
        return {"departments": []}
    return career_data

@career_router.get("/departments")
async def get_departments(current_user: dict = Depends(get_current_user)):
    """Get list of all departments"""
    career_data = await db.career_beetle.find_one({}, {"_id": 0})
    if not career_data:
        return []
    return [{"id": d["id"], "name": d["name"]} for d in career_data.get("departments", [])]

@career_router.get("/departments/{dept_id}")
async def get_department_roles(dept_id: str, current_user: dict = Depends(get_current_user)):
    """Get roles for a specific department"""
    career_data = await db.career_beetle.find_one({}, {"_id": 0})
    if not career_data:
        raise HTTPException(status_code=404, detail="Career data not found")
    
    for dept in career_data.get("departments", []):
        if dept["id"] == dept_id:
            return dept
    
    raise HTTPException(status_code=404, detail="Department not found")

@career_router.get("/my-path")
async def get_my_career_path(current_user: dict = Depends(get_current_user)):
    """Get the career path for the current user based on their role"""
    # For now, return a suggested path based on user's department if assigned
    user_dept = current_user.get("department", "sales")
    career_data = await db.career_beetle.find_one({}, {"_id": 0})
    
    if not career_data:
        return {"current_role": None, "next_steps": [], "department": None}
    
    for dept in career_data.get("departments", []):
        if dept["id"] == user_dept:
            return {
                "department": dept,
                "message": "Explore career progression within your department"
            }
    
    # Default to first department if user's dept not found
    return {
        "department": career_data["departments"][0] if career_data.get("departments") else None,
        "message": "Explore career opportunities"
    }

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
api_router.include_router(career_router)

# Include courses service router
from services.courses.routes import courses_router
api_router.include_router(courses_router, prefix="/courses-service")

app.include_router(api_router)

# Serve uploaded files (only if directory exists)
if UPLOADS_DIR.exists():
    app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="static_uploads")
    app.mount("/api/uploads", StaticFiles(directory=str(ROOT_DIR / "uploads")), name="uploads")

# Add a simple documents endpoint
@app.get("/api/documents/{filename}")
async def serve_document(filename: str):
    """Serve documents directly"""
    file_path = ROOT_DIR / "uploads" / "documents" / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Determine content type
    if filename.lower().endswith('.pdf'):
        media_type = "application/pdf"
    elif filename.lower().endswith('.docx'):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif filename.lower().endswith('.doc'):
        media_type = "application/msword"
    else:
        media_type = "application/octet-stream"
    
    async with aiofiles.open(file_path, 'rb') as f:
        content = await f.read()
    
    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f"inline; filename={filename}#toolbar=0&navpanes=0&scrollbar=0&view=FitH",
            "X-Frame-Options": "SAMEORIGIN",
            "Content-Security-Policy": "frame-ancestors 'self'"
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[origin.strip() for origin in os.environ.get('CORS_ORIGINS', '*').split(',')],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.get("/debug/lesson/{lesson_id}")
async def debug_lesson(lesson_id: str):
    lesson = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
    return {"found": lesson is not None, "lesson": lesson}

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
    
    # Only seed courses if no courses exist
    existing_courses = await db.courses.count_documents({})
    if existing_courses == 0:
        logger.info("No courses found. Seeding initial course data...")
        await seed_policy_courses()
    
    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("id", unique=True)
    await db.courses.create_index("id", unique=True)
    await db.modules.create_index("id", unique=True)
    await db.lessons.create_index("id", unique=True)
    await db.quizzes.create_index("id", unique=True)
    await db.progress.create_index([("user_id", 1), ("course_id", 1)])
    await db.certificates.create_index("id", unique=True)

async def seed_policy_courses():
    """Seed the 4 Flowitec policy courses with page-based content"""
    
    # Course 1: Leave Policy - Ghana
    leave_policy_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": leave_policy_id,
        "title": "Leave Policy - Ghana",
        "description": "The company recognizes the need for employees to rest, recharge and revitalize. This policy outlines the terms and conditions for requesting leave days at Flowitec Group Ltd.",
        "thumbnail": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400&h=225&fit=crop",
        "category": "HR Policy",
        "duration_hours": 1,
        "is_published": True,
        "course_type": "compulsory",
        "code": "LPHR1",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    leave_module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": leave_module_id,
        "course_id": leave_policy_id,
        "title": "Course Content",
        "description": "Complete content for Leave Policy - Ghana",
        "order": 0
    })
    
    leave_pages = [
        {"title": "Introduction to Leave Policy", "content": '''<div class="policy-page"><h2>LEAVE POLICY (LPHR1)</h2><h3>Introduction</h3><p>The company recognizes the need for employees to <strong>rest, recharge and revitalize</strong>, hence the leave policy.</p><p>The leave policy outlines the terms and conditions for requesting leave days here at Flowitec Group Ltd.</p><div class="highlight-box"><h4>Purpose</h4><p>To provide employees with time off from work for various reasons, while also ensuring that the organization's operational needs are met.</p></div><p class="legal-note">This policy shall be construed in accordance with the laws of Ghana, including but not limited to the <strong>Labour Act, 2003 (Act 651)</strong>.</p></div>'''},
        {"title": "Eligibility & Leave Request", "content": '''<div class="policy-page"><h2>Eligibility & Leave Request Process</h2><div class="policy-section"><h3>1. Eligibility</h3><p>Notwithstanding any other provision of this policy, all <strong>permanent/full-time employees</strong> of Flowitec shall be eligible for leave.</p><div class="warning-box"><p><strong>Exclusions:</strong> Persons who are on probation and performance improvement plans are not eligible. However, exemptions may be made considering the gravity of the emergency.</p></div></div><div class="policy-section"><h3>2. Leave Request</h3><p>An employee seeking to take leave shall submit a <strong>leave request form</strong> to their supervisor at least <strong>10 days prior</strong> to the commencement of the leave, unless in cases of emergency.</p></div><div class="policy-section"><h3>3. Approval</h3><p>The supervisor shall review the leave request and approve or deny it based on the operational needs of the business, in accordance with the Labour Act, 2003 (Act 651).</p></div></div>'''},
        {"title": "Leave Duration & Exemptions", "content": '''<div class="policy-page"><h2>Leave Duration & Emergency Exemptions</h2><div class="policy-section"><h3>4. Leave Duration</h3><div class="info-box"><p>Unless otherwise approved by the company, the maximum duration of leave that an employee can take at any time is <strong>five (5) consecutive working days</strong>.</p></div></div><div class="policy-section"><h3>5. Emergency Exemptions</h3><p>The Company may grant exemptions in exceptional emergency circumstances:</p><ul><li>Serious illness</li><li>Injury</li><li>Study leave for exams</li><li>Family bereavement</li></ul></div><div class="policy-section"><h3>6. Wellness Break</h3><p>These <strong>2 days leave</strong> shall be in addition to the employee's annual leave entitlement, taken in <strong>October</strong>.</p></div></div>'''},
        {"title": "Leave Administration", "content": '''<div class="policy-page"><h2>Leave Administration</h2><div class="policy-section"><h3>7. Leave Payment</h3><p>Annual leave shall be paid at the employee's <strong>regular rate of pay</strong>.</p></div><div class="policy-section"><h3>8. Leave Carryover</h3><p>Accrued annual leave shall be carried over up to a maximum of <strong>10 days</strong>.</p></div><div class="policy-section"><h3>9. Leave Record</h3><p>The HR department shall maintain accurate and confidential records.</p></div><div class="policy-section"><h3>10. Leave Cancellation</h3><p>Notify supervisor at least <strong>3 days prior</strong> to cancel a leave request.</p></div><div class="policy-section warning-box"><h3>11. Unapproved Leave</h3><p>Unauthorized leave may result in disciplinary action, up to and including termination.</p></div></div>'''},
        {"title": "Leave Types", "content": '''<div class="policy-page"><h2>Types of Leave</h2><div class="leave-type"><h3>1. Annual Leave</h3><div class="days-badge">21 Days</div><p>For vacation, personal or family purpose. Plus <strong>2 wellness days</strong> in October.</p></div><div class="leave-type"><h3>2. Sick Leave</h3><div class="days-badge">10 Days</div><p>For illness or injury. May be extended based on health conditions.</p></div><div class="leave-type"><h3>3. Bereavement Leave</h3><div class="days-badge">5 Days</div><p>For bereavement or funeral purposes.</p></div></div>'''},
        {"title": "Additional Leave Types", "content": '''<div class="policy-page"><h2>Additional Leave Types</h2><div class="leave-type"><h3>4. Maternity Leave</h3><div class="days-badge">12 Weeks</div><p>For childbirth or adoption purposes per Section 57 of the Labor Act, 2003.</p></div><div class="leave-type highlight"><h3>5. Wellness Break</h3><div class="days-badge special">2 Days</div><p>In recognition of mental health and well-being, taken in <strong>October</strong> for Mental Health Awareness Month.</p></div><div class="summary-box"><h4>Leave Summary</h4><ul><li><strong>Annual:</strong> 21 days + 2 wellness days</li><li><strong>Sick:</strong> 10 days</li><li><strong>Bereavement:</strong> 5 days</li><li><strong>Maternity:</strong> 12 weeks</li></ul></div></div>'''}
    ]
    
    for i, page in enumerate(leave_pages):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": leave_module_id,
            "title": page["title"],
            "content_type": "text",
            "content": page["content"],
            "duration_minutes": 5,
            "order": i
        })
    
    # Course 2: Code of Ethics & Conduct
    ethics_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": ethics_id,
        "title": "Code of Ethics & Conduct",
        "description": "At Flowitec, we are committed to conducting business with integrity, transparency, and respect for all individuals.",
        "thumbnail": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400&h=225&fit=crop",
        "category": "Ethics",
        "duration_hours": 1.5,
        "is_published": True,
        "course_type": "compulsory",
        "code": "CEPC3",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    ethics_module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": ethics_module_id,
        "course_id": ethics_id,
        "title": "Course Content",
        "order": 0
    })
    
    ethics_pages = [
        {"title": "Introduction", "content": '''<div class="policy-page"><h2>CODE OF ETHICS & CONDUCT</h2><p class="document-code">FLGG/232/72/CEPC3</p><h3>Introduction</h3><p>At Flowitec, we are committed to conducting business with <strong>integrity, transparency, and respect</strong> for all individuals.</p><div class="highlight-box"><p>This Code provides a framework for making ethical decisions and ensures we maintain a positive and professional environment.</p></div></div>'''},
        {"title": "Integrity and Honesty", "content": '''<div class="policy-page"><h2>1. Integrity and Honesty</h2><div class="principle-card"><ul><li>Conduct ourselves with the <strong>highest standards of integrity</strong></li><li>Be truthful in all communications</li><li>No deception, fraud, or misrepresentation</li></ul></div><h2>2. Respect for People</h2><div class="principle-card"><ul><li>Create a <strong>diverse and inclusive workplace</strong></li><li>No discrimination or harassment tolerated</li><li>Foster teamwork and open communication</li></ul></div></div>'''},
        {"title": "Fairness & Confidentiality", "content": '''<div class="policy-page"><h2>3. Fairness and Equal Opportunity</h2><div class="principle-card"><ul><li>Provide <strong>equal opportunity</strong> regardless of background</li><li>Decisions based on <strong>merit and performance</strong></li><li>Fair approach in all business practices</li></ul></div><h2>4. Confidentiality and Privacy</h2><div class="principle-card warning"><ul><li><strong>Protect confidential information</strong></li><li>Handle personal data with care</li><li>No use of information for personal gain</li></ul></div></div>'''},
        {"title": "Legal Compliance & Conflicts", "content": '''<div class="policy-page"><h2>5. Compliance with Laws</h2><div class="principle-card"><ul><li>Comply with all <strong>applicable laws and regulations</strong></li><li>Seek guidance from management when in doubt</li><li>Uphold ethical standards always</li></ul></div><h2>6. Conflicts of Interest</h2><div class="principle-card warning"><ul><li><strong>Avoid conflicts</strong> between personal and company interests</li><li>Disclose potential conflicts to supervisors</li><li>Gifts should not influence decisions</li></ul></div></div>'''},
        {"title": "Health, Safety & Accountability", "content": '''<div class="policy-page"><h2>7. Health, Safety, and Environment</h2><div class="principle-card"><ul><li>Provide <strong>safe and healthy workplace</strong></li><li>Minimize environmental impact</li><li>Report unsafe conditions immediately</li></ul></div><h2>8. Accountability</h2><div class="principle-card highlight"><ul><li><strong>Report unethical behavior</strong></li><li>Whistle-blowers protected from retaliation</li><li>Report through management or anonymous channels</li></ul></div></div>'''},
        {"title": "Financial Integrity & Excellence", "content": '''<div class="policy-page"><h2>9. Financial Integrity</h2><div class="principle-card"><ul><li>Financial records must be <strong>accurate and transparent</strong></li><li>No fraudulent reporting</li><li>Proper use of company resources</li></ul></div><h2>10. Commitment to Excellence</h2><div class="principle-card highlight"><ul><li>Strive for <strong>excellence</strong> in all work</li><li>Continuous improvement and innovation</li><li>Meet or exceed industry standards</li></ul></div></div>'''},
        {"title": "Gifts & Conclusion", "content": '''<div class="policy-page"><h2>11. Gifts and Favors</h2><div class="principle-card warning"><p>Employees <strong>will not solicit</strong> any gifts, bribes, favors, entertainment, loans, or items of monetary value from clients or suppliers.</p></div><h2>Conclusion</h2><div class="conclusion-box"><p>By adhering to this Code, we create a <strong>positive work environment</strong> supporting the success of the company, employees, and clients.</p><p class="emphasis">Each employee's commitment is vital to ensuring the <strong>long-term success and reputation</strong> of Flowitec.</p></div></div>'''}
    ]
    
    for i, page in enumerate(ethics_pages):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": ethics_module_id,
            "title": page["title"],
            "content_type": "text",
            "content": page["content"],
            "duration_minutes": 5,
            "order": i
        })
    
    # Course 3: Disciplinary Code
    disciplinary_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": disciplinary_id,
        "title": "Disciplinary Code",
        "description": "This code fosters a culture of care, mutual respect, and teamwork while ensuring fair and consistent treatment.",
        "thumbnail": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400&h=225&fit=crop",
        "category": "HR Policy",
        "duration_hours": 0.5,
        "is_published": True,
        "course_type": "compulsory",
        "code": "DCPC/HR1",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    disciplinary_module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": disciplinary_module_id,
        "course_id": disciplinary_id,
        "title": "Course Content",
        "order": 0
    })
    
    disciplinary_pages = [
        {"title": "Purpose of the Code", "content": '''<div class="policy-page"><h2>DISCIPLINARY CODE (DCPC/HR1)</h2><div class="info-box"><p>This document does not form part of any employment contract. All legal rights are reserved.</p></div><h3>Purpose of This Code</h3><div class="purpose-list"><div class="purpose-item"><span class="number">2.1</span><p>Foster a culture of <strong>care, mutual respect, and teamwork</strong></p></div><div class="purpose-item"><span class="number">2.2</span><p>Ensure <strong>fair and consistent treatment</strong> of all employees</p></div><div class="purpose-item"><span class="number">2.3</span><p>Provide a framework for <strong>collaboration</strong> between management and employees</p></div></div><div class="legal-note"><p>Works with The Code of Good Practice: Dismissal (Section 62, Labour Act, 2003).</p></div></div>'''},
        {"title": "Management Standards", "content": '''<div class="policy-page"><h2>Management Standards & Procedures</h2><div class="policy-section"><p><strong>4.</strong> Management sets standards for behavior and performance.</p></div><div class="policy-section"><p><strong>5.</strong> Minor issues addressed through:</p><ul><li>Counselling</li><li>PIPs (Performance Improvement Plans)</li><li>Warnings</li></ul></div><div class="policy-section warning-box"><p><strong>6.</strong> The Company reserves the right to <strong>terminate employment</strong> following fair procedure for conduct, performance, or capacity issues supported by clear evidence.</p></div></div>'''},
        {"title": "Gross Misconduct", "content": '''<div class="policy-page"><h2>7. Examples of Gross Misconduct</h2><div class="misconduct-grid"><div class="misconduct-item severe"><span class="number">7.1</span><p>Gross dishonesty</p></div><div class="misconduct-item severe"><span class="number">7.2</span><p>Willful damage of Company property</p></div><div class="misconduct-item severe"><span class="number">7.3</span><p>Physical assault on employer, employees, clients</p></div><div class="misconduct-item severe"><span class="number">7.4</span><p>Gross insubordination</p></div><div class="misconduct-item severe"><span class="number">7.5</span><p>Gross negligence</p></div><div class="misconduct-item severe"><span class="number">7.6</span><p>Misuse of drugs, alcohol</p></div><div class="misconduct-item severe"><span class="number">7.7</span><p>Sexual harassment</p></div></div><div class="warning-box"><p><strong>Note:</strong> May result in immediate dismissal following due process.</p></div></div>'''},
        {"title": "Unacceptable Behaviors", "content": '''<div class="policy-page"><h2>8. Unacceptable Behaviors</h2><div class="behavior-section"><h3>8.1 Obscene, immoral, or offensive conduct:</h3><ul><li>Sexual harassment</li><li>Racism, ethnocentrism, foul language</li><li>Rudeness to colleagues, clients, stakeholders</li></ul></div><div class="behavior-grid"><div class="behavior-item"><span class="number">8.2</span><p>Disloyalty</p></div><div class="behavior-item"><span class="number">8.3</span><p>Persistent absenteeism without leave</p></div><div class="behavior-item"><span class="number">8.4</span><p>Persistent late coming</p></div><div class="behavior-item"><span class="number">8.5</span><p>Insubordination</p></div><div class="behavior-item"><span class="number">8.6</span><p>Neglecting duties</p></div><div class="behavior-item"><span class="number">8.7</span><p>Failing to devote adequate attention</p></div></div></div>'''}
    ]
    
    for i, page in enumerate(disciplinary_pages):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": disciplinary_module_id,
            "title": page["title"],
            "content_type": "text",
            "content": page["content"],
            "duration_minutes": 5,
            "order": i
        })
    
    # Course 4: Health & Safety Policy
    safety_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": safety_id,
        "title": "Health & Safety Policy",
        "description": "Flowitec is committed to maintaining a safe and healthy workplace for all employees and visitors.",
        "thumbnail": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=400&h=225&fit=crop",
        "category": "Safety",
        "duration_hours": 1,
        "is_published": True,
        "course_type": "compulsory",
        "code": "H/SP1",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    safety_module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": safety_module_id,
        "course_id": safety_id,
        "title": "Course Content",
        "order": 0
    })
    
    safety_pages = [
        {"title": "Policy Overview", "content": '''<div class="policy-page"><h2>HEALTH & SAFETY POLICY</h2><p class="document-code">Policy No: H/SP 1</p><div class="purpose-box"><h3>Purpose</h3><ul><li>Prevent accidents and injuries</li><li>Comply with statutory requirements</li><li>Ensure proper handling and storage</li><li>Provide safety-first culture</li><li>Provide adequate training</li></ul></div><div class="policy-statement highlight-box"><h3>POLICY</h3><p>Flowitec is committed to maintaining a <strong>safe and healthy workplace</strong> for all employees and visitors.</p></div><div class="legal-note"><p>Enacted per <strong>Labour Act, 2003 (Act 651)</strong> and <strong>Factories, Offices and Shops Act, 1970</strong>.</p></div></div>'''},
        {"title": "Safety Guidelines", "content": '''<div class="policy-page"><h2>Policy Guidelines</h2><h3>Warehouse Safety</h3><div class="guideline-item"><span class="number">1.</span><p>Warehouse access <strong>restricted to authorized personnel</strong></p></div><div class="guideline-item important"><span class="number">2.</span><p><strong>Required PPE:</strong> High-visibility vests, safety boots, gloves, helmets</p></div><div class="guideline-item"><span class="number">3.</span><p>All staff must <strong>sign in and out</strong></p></div><div class="guideline-item"><span class="number">4.</span><p>Use pallet jacks, forklifts for heavy lifting. Manual lifting should be minimized.</p></div><h3>Office Safety</h3><div class="guideline-item"><span class="number">5.</span><p>Electrical equipment grounded. Fire extinguishers mounted. Flammable materials in ventilated areas.</p></div></div>'''},
        {"title": "Emergency Procedures", "content": '''<div class="policy-page"><h2>Policy Procedures</h2><div class="procedure-grid"><div class="procedure-item"><span class="number">1.</span><p><strong>Emergency contacts</strong> must be provided by all staff</p></div><div class="procedure-item"><span class="number">2.</span><p><strong>First aid kits</strong> must be stocked and accessible</p></div><div class="procedure-item"><span class="number">3.</span><p><strong>One senior staff</strong> on duty during warehouse activities</p></div><div class="procedure-item important"><span class="number">4.</span><p>All injuries and near misses <strong>reported immediately</strong> to HR</p></div><div class="procedure-item"><span class="number">5.</span><p><strong>Incident reports</strong> shared with supervisor and manager</p></div></div></div>'''},
        {"title": "Training & Supervision", "content": '''<div class="policy-page"><h2>6. Training and Supervision</h2><div class="training-section"><div class="training-item"><span class="number">6.1</span><p>New employees undergo <strong>safety induction training</strong></p></div><div class="training-item"><span class="number">6.2</span><p><strong>Regular refresher training</strong> for all staff</p></div><div class="training-item"><span class="number">6.3</span><p><strong>Weekly risk meetings</strong></p></div><div class="training-item"><span class="number">6.4</span><p>Supervisors ensure compliance</p></div></div><h2>7. Monitoring and Review</h2><div class="monitoring-section"><div class="monitoring-item"><span class="number">7.1</span><p>Risk assessment reviewed <strong>annually</strong> or after incidents</p></div><div class="monitoring-item"><span class="number">7.2</span><p>Policy updated annually</p></div></div></div>'''},
        {"title": "Penalties", "content": '''<div class="policy-page"><h2>8. Penalties for Non-Compliance</h2><div class="legal-reference"><p>Per <strong>Section 118(2) of the Labour Act, 2003</strong></p></div><div class="penalty-section"><h3>8.1 Minor Infractions</h3><p class="examples">Not wearing PPE, unauthorized movement</p><ul><li>Verbal warning</li><li>Mandatory retraining</li></ul></div><div class="penalty-section moderate"><h3>8.2 Moderate Infractions</h3><p class="examples">Repeated neglect, improper equipment use</p><ul><li>Written warning</li><li>Temporary suspension</li></ul></div><div class="penalty-section severe"><h3>8.3 Major Infractions</h3><p class="examples">Tampering with safety equipment, failure to report</p><ul><li>Final warning</li><li>Suspension without pay</li><li>Termination</li></ul></div></div>'''},
        {"title": "Roles & Responsibilities", "content": '''<div class="policy-page"><h2>Roles And Responsibilities</h2><div class="role-section"><h3>1. Management Must:</h3><ul><li>Conduct risk assessments and safety audits</li><li>Ensure PPE is provided and worn</li><li>Implement safe work procedures</li><li>Offer safety training</li></ul></div><div class="role-section"><h3>2. Employees Must:</h3><ul><li>Follow safety procedures and wear PPE</li><li>Report hazards immediately</li><li>Attend mandatory training</li><li>Operate equipment only if trained</li></ul></div><div class="role-section"><h3>3. Visitors Must:</h3><ul><li>Follow all safety rules</li><li>Be accompanied in operational areas</li><li>Report unsafe conditions</li></ul></div><div class="declaration-box"><h3>Declaration</h3><p>Flowitec is committed to creating a culture where <strong>safety is a shared responsibility</strong>.</p></div></div>'''}
    ]
    
    for i, page in enumerate(safety_pages):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": safety_module_id,
            "title": page["title"],
            "content_type": "text",
            "content": page["content"],
            "duration_minutes": 5,
            "order": i
        })
    
    # Seed Career Beetle data
    await db.career_beetle.delete_many({})
    await db.career_beetle.insert_one({
        "departments": [
            {"id": "sales", "name": "SALES", "roles": [
                {"id": "vp_sales", "title": "VP - Sales", "level": "Senior Mgt.", "key_skills": "Leadership, strategic sales planning", "qualifications": "MBA, 10+ years", "timeline": "N/A"},
                {"id": "country_sales_mgr", "title": "Country Sales Manager", "level": "First Level", "key_skills": "Sales strategy, business development", "qualifications": "Bachelor's/MBA, 7+ years", "timeline": "3-5 years"},
                {"id": "tech_sales_mgr", "title": "Technical Sales Manager", "level": "First Level", "key_skills": "Solutions sharing, technical advisory", "qualifications": "Engineering, 5+ years", "timeline": "3-4 years"},
                {"id": "sr_sales_eng", "title": "Senior Sales Engineer", "level": "Mid level", "key_skills": "Technical expertise, client relationships", "qualifications": "Engineering, 4+ years", "timeline": "2-3 years"},
                {"id": "sales_eng", "title": "Sales Engineer", "level": "Intermediate", "key_skills": "Product knowledge, customer service", "qualifications": "Engineering, 1-2 years", "timeline": "1-2 years"},
                {"id": "sales_trainee", "title": "Sales Trainee", "level": "Entry level", "key_skills": "Learn products, shadow calls", "qualifications": "Engineering, Fresh graduate", "timeline": "6-12 months"}
            ]},
            {"id": "supply_chain", "name": "SUPPLY CHAIN", "roles": [
                {"id": "coo", "title": "COO - Supply Chain", "level": "Senior Level", "key_skills": "Executive decision making, logistics", "qualifications": "MBA, 15+ years", "timeline": "N/A"},
                {"id": "procurement_mgr", "title": "Procurement Manager", "level": "First Level", "key_skills": "Excel, project management", "qualifications": "Bachelor's, 5+ years", "timeline": "3-4 years"},
                {"id": "sr_procurement", "title": "Senior Procurement Officer", "level": "Mid level", "key_skills": "Inventory controls, reporting", "qualifications": "Bachelor's, 3+ years", "timeline": "2-3 years"},
                {"id": "procurement_off", "title": "Procurement Officer", "level": "Intermediate", "key_skills": "Basic procurement knowledge", "qualifications": "Bachelor's, 1-2 years", "timeline": "1-2 years"}
            ]},
            {"id": "finance", "name": "FINANCE", "roles": [
                {"id": "cfo", "title": "CFO", "level": "Senior Level", "key_skills": "Strategic planning, risk management", "qualifications": "MBA/CPA, 15+ years", "timeline": "N/A"},
                {"id": "finance_mgr", "title": "Finance Manager", "level": "Senior Mgt.", "key_skills": "Financial modeling, compliance", "qualifications": "CPA/ACCA, 8+ years", "timeline": "4-5 years"},
                {"id": "sr_accountant", "title": "Senior Accountant", "level": "First Level", "key_skills": "Financial reporting, budgeting", "qualifications": "Bachelor's/CPA, 5+ years", "timeline": "3-4 years"},
                {"id": "accountant", "title": "Accountant", "level": "Mid level", "key_skills": "Advanced accounting, analysis", "qualifications": "Bachelor's, 3+ years", "timeline": "2-3 years"}
            ]},
            {"id": "hr", "name": "HUMAN RESOURCE", "roles": [
                {"id": "hr_director", "title": "HR Director", "level": "Senior Level", "key_skills": "Strategic workforce planning", "qualifications": "MBA/MHRM, 12+ years", "timeline": "N/A"},
                {"id": "hr_mgr", "title": "HR Manager", "level": "Senior Mgt.", "key_skills": "Talent management, policy development", "qualifications": "Bachelor's/Masters, 7+ years", "timeline": "4-5 years"},
                {"id": "sr_hr_off", "title": "Senior HR Officer", "level": "First Level", "key_skills": "Recruitment, employee relations", "qualifications": "Bachelor's, 4+ years", "timeline": "2-3 years"},
                {"id": "hr_off", "title": "HR Officer", "level": "Mid level", "key_skills": "HRIS, HR policies", "qualifications": "Bachelor's, 2+ years", "timeline": "1-2 years"}
            ]},
            {"id": "facilities", "name": "FACILITIES", "roles": [
                {"id": "facilities_mgr", "title": "Facilities Manager", "level": "Senior Mgt.", "key_skills": "Facilities strategy, health and safety", "qualifications": "Bachelor's, 7+ years", "timeline": "N/A"},
                {"id": "facilities_super", "title": "Facilities Supervisor", "level": "First Level", "key_skills": "Team leadership, maintenance", "qualifications": "Diploma, 4+ years", "timeline": "3-4 years"},
                {"id": "facilities_off", "title": "Facilities Officer", "level": "Mid level", "key_skills": "Office supplies, maintenance", "qualifications": "Diploma, 2+ years", "timeline": "2 years"}
            ]}
        ]
    })
    
    logger.info("Seeded 4 policy courses with page-based content and Career Beetle data")
@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
