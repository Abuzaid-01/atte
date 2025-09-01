
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import date
# from ..database import get_db
# from .. import models, schemas
# from ..auth.utils import get_current_teacher

# router = APIRouter()

# @router.post("/quick")
# def quick_mark(payload: schemas.QuickAttendanceCreate, db: Session = Depends(get_db), me: models.Teacher = Depends(get_current_teacher)):
#     today = payload.date or date.today()
    
#     # Find student by roll number in the classroom
#     student = db.query(models.Student).filter(
#         models.Student.classroom_id == payload.classroom_id,
#         models.Student.roll_no == payload.roll_no
#     ).first()
    
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
    
#     # Check if classroom belongs to current teacher
#     classroom = db.get(models.Classroom, payload.classroom_id)
#     if not classroom or classroom.teacher_id != me.id:
#         raise HTTPException(status_code=404, detail="Classroom not found")
    
#     # Check if attendance already exists for this student on this date
#     existing_attendance = db.query(models.Attendance).filter(
#         models.Attendance.student_id == student.id,
#         models.Attendance.date == today
#     ).first()
    
#     # Get status from payload, default to 'present' if not provided
#     status = getattr(payload, 'status', models.AttendanceStatus.present)
    
#     if existing_attendance:
#         # Update existing attendance
#         existing_attendance.status = status
#         db.commit()
#         return {"message": f"Roll {payload.roll_no} updated to {status.value}", "date": str(today)}
#     else:
#         # Create new attendance record
#         attendance = models.Attendance(
#             date=today,
#             status=status,  # Use the status from payload
#             student_id=student.id,
#             classroom_id=payload.classroom_id,
#             teacher_id=me.id
#         )
#         db.add(attendance)
#         db.commit()
#         return {"message": f"Roll {payload.roll_no} marked {status.value}", "date": str(today)}
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from ..database import get_db
from .. import models, schemas
from ..auth.utils import get_current_teacher

router = APIRouter()

@router.post("/quick")
def quick_mark(payload: schemas.QuickAttendanceCreate, db: Session = Depends(get_db), me: models.Teacher = Depends(get_current_teacher)):
    # Parse date - handle both string and None
    if payload.date:
        try:
            today = date.fromisoformat(payload.date)
        except:
            today = date.today()
    else:
        today = date.today()
    
    # Find student by roll number in the classroom
    student = db.query(models.Student).filter(
        models.Student.classroom_id == payload.classroom_id,
        models.Student.roll_no == payload.roll_no
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if classroom belongs to current teacher
    classroom = db.get(models.Classroom, payload.classroom_id)
    if not classroom or classroom.teacher_id != me.id:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    # Check if attendance already exists for this student on this date
    existing_attendance = db.query(models.Attendance).filter(
        models.Attendance.student_id == student.id,
        models.Attendance.date == today
    ).first()
    
    # Convert string status to enum
    status_str = payload.status or "present"
    try:
        if status_str.lower() == "present":
            status = models.AttendanceStatus.present
        elif status_str.lower() == "absent":
            status = models.AttendanceStatus.absent
        else:
            status = models.AttendanceStatus.present  # Default fallback
    except:
        status = models.AttendanceStatus.present  # Default fallback
    
    if existing_attendance:
        # Update existing attendance
        existing_attendance.status = status
        db.commit()
        return {"message": f"Roll {payload.roll_no} updated to {status.value}", "date": str(today)}
    else:
        # Create new attendance record
        attendance = models.Attendance(
            date=today,
            status=status,  # Use the status from payload
            student_id=student.id,
            classroom_id=payload.classroom_id,
            teacher_id=me.id
        )
        db.add(attendance)
        db.commit()
        return {"message": f"Roll {payload.roll_no} marked {status.value}", "date": str(today)}

# NEW GET ENDPOINTS FOR VIEWING ATTENDANCE

@router.get("/{classroom_id}")
def get_attendance(
    classroom_id: int,
    attendance_date: Optional[date] = Query(None, alias="date"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    me: models.Teacher = Depends(get_current_teacher)
):
    """Get attendance records for a classroom"""
    
    # Check if classroom belongs to current teacher
    classroom = db.get(models.Classroom, classroom_id)
    if not classroom or classroom.teacher_id != me.id:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    # Build query
    query = db.query(models.Attendance).filter(models.Attendance.classroom_id == classroom_id)
    
    # Filter by date(s)
    if attendance_date:
        query = query.filter(models.Attendance.date == attendance_date)
    elif start_date and end_date:
        query = query.filter(models.Attendance.date.between(start_date, end_date))
    elif start_date:
        query = query.filter(models.Attendance.date >= start_date)
    elif end_date:
        query = query.filter(models.Attendance.date <= end_date)
    else:
        # Default to today if no date specified
        today = date.today()
        query = query.filter(models.Attendance.date == today)
    
    # Get attendance records with student information
    attendance_records = query.join(models.Student).all()
    
    # Format response
    result = []
    for record in attendance_records:
        result.append({
            "id": record.id,
            "date": str(record.date),
            "status": record.status.value,
            "student_id": record.student_id,
            "student": {
                "id": record.student_id,
                "roll_no": db.get(models.Student, record.student_id).roll_no,
                "name": db.get(models.Student, record.student_id).name,
                "email": db.get(models.Student, record.student_id).email,
            }
        })
    
    return result

@router.get("/{classroom_id}/summary")
def get_attendance_summary(
    classroom_id: int,
    attendance_date: Optional[date] = Query(None, alias="date"),
    db: Session = Depends(get_db),
    me: models.Teacher = Depends(get_current_teacher)
):
    """Get attendance summary with all students and their status"""
    
    # Check if classroom belongs to current teacher
    classroom = db.get(models.Classroom, classroom_id)
    if not classroom or classroom.teacher_id != me.id:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    target_date = attendance_date or date.today()
    
    # Get all students in classroom
    students = db.query(models.Student).filter(models.Student.classroom_id == classroom_id).order_by(models.Student.roll_no).all()
    
    # Get attendance for the date
    attendance_records = db.query(models.Attendance).filter(
        models.Attendance.classroom_id == classroom_id,
        models.Attendance.date == target_date
    ).all()
    
    # Create attendance lookup
    attendance_lookup = {record.student_id: record.status.value for record in attendance_records}
    
    # Build summary
    summary = {
        "date": str(target_date),
        "classroom_id": classroom_id,
        "classroom_name": classroom.name,
        "subject": classroom.subject,
        "total_students": len(students),
        "present_count": sum(1 for status in attendance_lookup.values() if status == "present"),
        "absent_count": sum(1 for status in attendance_lookup.values() if status == "absent"),
        "not_marked_count": len(students) - len(attendance_lookup),
        "students": []
    }
    
    for student in students:
        status = attendance_lookup.get(student.id, "not_marked")
        summary["students"].append({
            "id": student.id,
            "roll_no": student.roll_no,
            "name": student.name,
            "email": student.email,
            "status": status
        })
    
    return summary