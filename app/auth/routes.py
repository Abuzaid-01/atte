from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models, schemas
from .utils import hash_password, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter()

# Simple student model for direct registration
class StudentCreate(BaseModel):
    name: str
    email: str
    password: str
    student_id: str

@router.get("/test-create-user")
def test_create_user(db: Session = Depends(get_db)):
    """Create a test user for debugging"""
    # Check if test user already exists
    if db.query(models.Teacher).filter(models.Teacher.email == "test@example.com").first():
        return {"message": "Test user already exists", "email": "test@example.com", "password": "password123"}
    
    # Create test user
    t = models.Teacher(
        name="Test Teacher", 
        email="test@example.com", 
        password_hash=hash_password("password123")
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"message": "Created test user", "email": "test@example.com", "password": "password123"}

@router.post("/signup", response_model=schemas.TeacherOut)
def signup(payload: schemas.TeacherSignup, db: Session = Depends(get_db)):
    if db.query(models.Teacher).filter(models.Teacher.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    t = models.Teacher(name=payload.name, email=payload.email, password_hash=hash_password(payload.password))
    db.add(t); db.commit(); db.refresh(t)
    return t

# Simple direct student registration endpoint
@router.post("/signup/student")
def student_signup(student: StudentCreate, db: Session = Depends(get_db)):
    """Simplified endpoint for registering students"""
    # Check if email already exists
    if db.query(models.Student).filter(models.Student.email == student.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if student_id already exists
    if db.query(models.Student).filter(models.Student.student_id == student.student_id).first():
        raise HTTPException(status_code=400, detail="Student ID already registered")
    
    # Create student
    s = models.Student(
        name=student.name,
        email=student.email,
        password_hash=hash_password(student.password),
        student_id=student.student_id
    )
    
    try:
        db.add(s)
        db.commit()
        db.refresh(s)
        return {"message": "Student registered successfully", "id": s.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    t = db.query(models.Teacher).filter(models.Teacher.email == form.username).first()
    if not t or not verify_password(form.password, t.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": str(t.id)})
    return {"access_token": token, "token_type": "bearer"}
