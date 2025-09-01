from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ..database import get_db
from .. import models, schemas
from ..auth.utils import get_current_teacher
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=schemas.ClassroomOut, status_code=status.HTTP_201_CREATED)
def create_classroom(payload: schemas.ClassroomCreate, db: Session = Depends(get_db), me: models.Teacher = Depends(get_current_teacher)):
    logger.info(f"Creating classroom: {payload.name}, {payload.subject} for teacher_id: {me.id}")
    try:
        # Check if class with the same name already exists for this teacher
        existing = db.query(models.Classroom).filter(
            models.Classroom.name == payload.name,
            models.Classroom.teacher_id == me.id
        ).first()
        
        if existing:
            logger.warning(f"Class with name {payload.name} already exists for teacher {me.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A class with name '{payload.name}' already exists"
            )
        
        # Create new classroom
        c = models.Classroom(
            name=payload.name, 
            subject=payload.subject, 
            teacher_id=me.id
        )
        
        db.add(c)
        db.commit()
        db.refresh(c)
        
        logger.info(f"Classroom created successfully: {c.id}")
        return c
        
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Database integrity error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error. Class creation failed."
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in create_classroom: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get("/", response_model=list[schemas.ClassroomOut])
def my_classrooms(db: Session = Depends(get_db), me: models.Teacher = Depends(get_current_teacher)):
    logger.info(f"Fetching classrooms for teacher_id: {me.id}")
    try:
        classrooms = db.query(models.Classroom).filter(models.Classroom.teacher_id == me.id).all()
        logger.info(f"Found {len(classrooms)} classrooms")
        return classrooms
    except Exception as e:
        logger.error(f"Error fetching classrooms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve classrooms"
        )

