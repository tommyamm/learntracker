from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import CollectorRegistry
import time
from functools import wraps
from sqlalchemy.orm import Session
from . import models

# Создаем собственный реестр метрик
REGISTRY = CollectorRegistry()

# Метрики HTTP запросов
http_requests_total = Counter(
    'learntracker_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status'],
    registry=REGISTRY
)

http_request_duration = Histogram(
    'learntracker_http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
    registry=REGISTRY
)

# Метрики БД
db_queries_total = Counter(
    'learntracker_db_queries_total',
    'Total database queries',
    ['operation'],
    registry=REGISTRY
)

db_connections_active = Gauge(
    'learntracker_db_connections_active',
    'Active database connections',
    registry=REGISTRY
)

# Бизнес-метрики
courses_total = Gauge(
    'learntracker_courses_total',
    'Total number of courses',
    registry=REGISTRY
)

students_total = Gauge(
    'learntracker_students_total',
    'Total number of students',
    registry=REGISTRY
)

lesson_completions_total = Counter(
    'learntracker_lesson_completions_total',
    'Total number of completed lessons',
    registry=REGISTRY
)

submissions_total = Counter(
    'learntracker_submissions_total',
    'Total number of submissions',
    ['status'],
    registry=REGISTRY
)

# Декоратор для мониторинга HTTP запросов
def monitor_requests(endpoint: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status = "200"
            method = "GET"  # По умолчанию, можно улучшить
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = "500"
                raise
            finally:
                # Записываем метрики
                duration = time.time() - start_time
                http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
                http_request_duration.labels(method=method, endpoint=endpoint).observe(duration)
        
        return wrapper
    return decorator

# Декоратор для мониторинга БД операций
def monitor_db_operation(operation: str):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                db_queries_total.labels(operation=operation).inc()
                return result
            except Exception as e:
                db_queries_total.labels(operation=f"{operation}_error").inc()
                raise
                
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                db_queries_total.labels(operation=operation).inc()
                return result
            except Exception as e:
                db_queries_total.labels(operation=f"{operation}_error").inc()
                raise
        
        # Проверяем, является ли функция асинхронной
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
            
    return decorator

# Функция для обновления бизнес-метрик
def update_business_metrics(db: Session):
    """Обновляет бизнес-метрики из БД"""
    try:
        # Количество курсов
        courses_count = db.query(models.Course).count()
        courses_total.set(courses_count)
        
        # Количество студентов
        students_count = db.query(models.Student).count()
        students_total.set(students_count)
        
        # Активные подключения к БД (примерное значение)
        db_connections_active.set(db.get_bind().pool.checkedout())
        
    except Exception as e:
        print(f"Error updating business metrics: {e}")

# Функция для экспорта метрик
def get_metrics():
    """Возвращает метрики в формате Prometheus"""
    return generate_latest(REGISTRY)

# Функции для инкремента специфичных метрик
def increment_lesson_completion():
    lesson_completions_total.inc()

def increment_submission(status: str = "pending"):
    submissions_total.labels(status=status).inc()