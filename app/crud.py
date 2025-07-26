from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from . import models, schemas
from typing import List, Optional
import time

# CRUD для курсов
def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

# CRUD для студентов
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()

# CRUD для записи на курсы
def enroll_student(db: Session, course_id: int, student_id: int):
    # Проверяем, не записан ли уже студент
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == course_id,
        models.Enrollment.student_id == student_id
    ).first()
    
    if existing:
        return None  # Уже записан
    
    enrollment = models.Enrollment(course_id=course_id, student_id=student_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

# CRUD для уроков
def get_course_lessons(db: Session, course_id: int):
    return db.query(models.Lesson).filter(
        models.Lesson.course_id == course_id
    ).order_by(models.Lesson.order_num).all()

def create_lesson(db: Session, course_id: int, lesson: schemas.LessonBase):
    db_lesson = models.Lesson(**lesson.dict(), course_id=course_id)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

# CRUD для прохождения уроков
def complete_lesson(db: Session, lesson_id: int, completion: schemas.LessonCompletionCreate):
    # Проверяем, не пройден ли уже урок
    existing = db.query(models.LessonCompletion).filter(
        models.LessonCompletion.lesson_id == lesson_id,
        models.LessonCompletion.student_id == completion.student_id
    ).first()
    
    if existing:
        return None  # Уже пройден
    
    db_completion = models.LessonCompletion(
        lesson_id=lesson_id,
        student_id=completion.student_id,
        time_spent=completion.time_spent
    )
    db.add(db_completion)
    db.commit()
    db.refresh(db_completion)
    return db_completion

# CRUD для решений
def create_submission(db: Session, submission: schemas.SubmissionCreate):
    db_submission = models.Submission(**submission.dict())
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def get_submissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Submission).offset(skip).limit(limit).all()

# Аналитика (медленные запросы для тестирования алертов)
def get_course_analytics(db: Session):
    """Сложный запрос для аналитики курсов - будет медленным при нагрузке"""
    time.sleep(0.1)  # Искусственная задержка для демонстрации
    
    result = db.query(
        models.Course.id,
        models.Course.title,
        func.count(models.Enrollment.id).label('total_students'),
        func.count(models.LessonCompletion.id).label('completed_lessons'),
        func.avg(models.LessonCompletion.time_spent).label('avg_completion_time')
    ).outerjoin(
        models.Enrollment, models.Course.id == models.Enrollment.course_id
    ).outerjoin(
        models.Lesson, models.Course.id == models.Lesson.course_id
    ).outerjoin(
        models.LessonCompletion, models.Lesson.id == models.LessonCompletion.lesson_id
    ).group_by(models.Course.id, models.Course.title).all()
    
    return [
        schemas.CourseAnalytics(
            course_id=row[0],
            course_title=row[1],
            total_students=row[2] or 0,
            completed_lessons=row[3] or 0,
            avg_completion_time=float(row[4]) if row[4] else None
        )
        for row in result
    ]

def get_student_progress(db: Session, student_id: int):
    """Прогресс конкретного студента"""
    time.sleep(0.05)  # Небольшая задержка
    
    # Количество записей на курсы
    enrollments_count = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id
    ).count()
    
    # Количество пройденных уроков
    completed_lessons = db.query(models.LessonCompletion).filter(
        models.LessonCompletion.student_id == student_id
    ).count()
    
    # Общее количество доступных уроков в записанных курсах
    total_lessons = db.query(models.Lesson).join(
        models.Enrollment, models.Lesson.course_id == models.Enrollment.course_id
    ).filter(models.Enrollment.student_id == student_id).count()
    
    student = get_student(db, student_id)
    
    completion_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    return schemas.StudentProgress(
        student_id=student_id,
        student_name=student.name if student else "Unknown",
        total_enrollments=enrollments_count,
        completed_lessons=completed_lessons,
        completion_percentage=round(completion_percentage, 2)
    )