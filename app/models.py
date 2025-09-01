from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
import enum

class AttendanceStatus(str, enum.Enum):
    present = "present"
    absent = "absent"

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    classrooms = relationship("Classroom", back_populates="teacher")

class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)        # e.g., "10A"
    subject = Column(String, nullable=False)     # e.g., "Maths"
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    teacher = relationship("Teacher", back_populates="classrooms")
    students = relationship("Student", back_populates="classroom", cascade="all, delete-orphan")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    roll_no = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)

    classroom = relationship("Classroom", back_populates="students")
    __table_args__ = (
        UniqueConstraint("classroom_id", "roll_no", name="uq_class_roll"),
    )

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    # optional: a unique per day per student constraint if you want
    __table_args__ = (
        UniqueConstraint("student_id", "date", name="uq_student_date"),
    )
