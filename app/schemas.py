

    

from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional, List, Literal, Union
from .models import AttendanceStatus

# Auth
class TeacherSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class TeacherOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Classroom
class ClassroomCreate(BaseModel):
    name: str
    subject: str

class ClassroomOut(BaseModel):
    id: int
    name: str
    subject: str
    class Config:
        from_attributes = True

# Student
class StudentCreate(BaseModel):
    roll_no: int
    name: str
    email: Optional[EmailStr] = None

class StudentOut(BaseModel):
    id: int
    roll_no: int
    name: str
    email: Optional[EmailStr]
    class Config:
        from_attributes = True

# Attendance
class QuickMarkIn(BaseModel):
    classroom_id: int
    roll_no: int
    date: Optional[date] = None   # default today handled in route

class QuickAttendanceCreate(BaseModel):
    classroom_id: int
    roll_no: int
    date: Optional[str] = None  # Accept as string, parse in route
    status: Optional[str] = "present"

class BulkEntry(BaseModel):
    roll_no: int
    status: Literal["present", "absent"]

class BulkMarkIn(BaseModel):
    classroom_id: int
    entries: List[BulkEntry]
    date: Optional[str] = None  # Accept as string, parse in route