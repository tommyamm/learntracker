from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# Базовые схемы
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None
    order_num: int

class Lesson(LessonBase):
    id: int
    course_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    student_id: int

class LessonCompletionCreate(BaseModel):
    student_id: int
    time_spent: Optional[int] = None

class SubmissionCreate(BaseModel):
    student_id: int
    lesson_id: int
    content: str

class Submission(BaseModel):
    id: int
    student_id: int
    lesson_id: int
    content: str
    status: str
    submitted_at: datetime
    
    class Config:
        from_attributes = True

# Схемы для аналитики
class CourseAnalytics(BaseModel):
    course_id: int
    course_title: str
    total_students: int
    completed_lessons: int
    avg_completion_time: Optional[float] = None

class StudentProgress(BaseModel):
    student_id: int
    student_name: str
    total_enrollments: int
    completed_lessons: int
    completion_percentage: float