from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth.utils import get_current_teacher

router = APIRouter()

@router.post("/{classroom_id}", response_model=schemas.StudentOut)
def add_student(classroom_id: int, payload: schemas.StudentCreate, db: Session = Depends(get_db), me: models.Teacher = Depends(get_current_teacher)):
    classroom = db.get(models.Classroom, classroom_id)
    if not classroom or classroom.teacher_id != me.id:
        raise HTTPException(status_code=404, detail="Classroom not found")
    s = models.Student(roll_no=payload.roll_no, name=payload.name, email=payload.email, classroom_id=classroom_id)
    db.add(s); db.commit(); db.refresh(s)
    return s

@router.get("/{classroom_id}", response_model=list[schemas.StudentOut])
def list_students(classroom_id: int, db: Session = Depends(get_db), me: models.Teacher = Depends(get_current_teacher)):
    classroom = db.get(models.Classroom, classroom_id)
    if not classroom or classroom.teacher_id != me.id:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return db.query(models.Student).filter(models.Student.classroom_id == classroom_id).order_by(models.Student.roll_no).all()
