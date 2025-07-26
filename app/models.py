from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course")

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    order_num = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    course = relationship("Course", back_populates="lessons")
    completions = relationship("LessonCompletion", back_populates="lesson")
    submissions = relationship("Submission", back_populates="lesson")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    enrollments = relationship("Enrollment", back_populates="student")
    completions = relationship("LessonCompletion", back_populates="student")
    submissions = relationship("Submission", back_populates="student")

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Уникальность: студент не может записаться на курс дважды
    __table_args__ = (UniqueConstraint('student_id', 'course_id'),)
    
    # Связи
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class LessonCompletion(Base):
    __tablename__ = "lesson_completions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    time_spent = Column(Integer)  # в секундах
    
    # Уникальность: урок можно пройти только один раз
    __table_args__ = (UniqueConstraint('student_id', 'lesson_id'),)
    
    # Связи
    student = relationship("Student", back_populates="completions")
    lesson = relationship("Lesson", back_populates="completions")

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(50), default="pending")
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True))
    
    # Связи
    student = relationship("Student", back_populates="submissions")
    lesson = relationship("Lesson", back_populates="submissions")