from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, PlainTextResponse
from sqlalchemy.orm import Session
from typing import List
import time
import uvicorn

from . import crud, models, schemas, metrics
from .database import SessionLocal, engine, get_db

# Создаем таблицы в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LearnTracker API",
    description="Educational platform for tracking learning progress",
    version="1.0.0"
)

# Middleware для мониторинга всех запросов
@app.middleware("http")
async def monitor_requests_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    # Записываем метрики
    duration = time.time() - start_time
    endpoint = request.url.path
    method = request.method
    status = str(response.status_code)
    
    metrics.http_requests_total.labels(
        method=method, 
        endpoint=endpoint, 
        status=status
    ).inc()
    
    metrics.http_request_duration.labels(
        method=method, 
        endpoint=endpoint
    ).observe(duration)
    
    return response

# HTML документация
DOCS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LearnTracker API Documentation</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .content {
            padding: 30px;
        }
        .endpoint {
            background: #f8f9fa;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }
        .method {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            color: white;
            margin-right: 10px;
        }
        .method-GET { background: #28a745; }
        .method-POST { background: #007bff; }
        .code {
            background: #f1f3f4;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            margin: 10px 0;
            overflow-x: auto;
        }
        .note {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
        }
        .load-test {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
        }
    </style>
</head>
<body>ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If
    <div class="container">
        <div class="header">
            <h1>📚 LearnTracker API</h1>
            <p>Educational Platform for Progress Tracking</p>
        </div>
        <div class="content">
            <div class="note">
                <strong>✅ Status:</strong> Application is running with PostgreSQL database
            </div>
            
            <div class="load-test">
                <strong>🔧 Load Testing:</strong> 
                <a href="/load-test" target="_blank">Open Load Testing UI</a> |
                <a href="/metrics" target="_blank">View Metrics</a>
            </div>
            
            <h2>🏥 Health & Monitoring</h2>
            
            <div class="endpoint">
                <h3><span class="method method-GET">GET</span>/health</h3>
                <p>Application health check</p>
                <div class="code">curl http://localhost:8000/health</div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method method-GET">GET</span>/metrics</h3>
                <p>Prometheus metrics endpoint</p>
                <div class="code">curl http://localhost:8000/metrics</div>
            </div>
            
            <h2>👨‍🎓 Students</h2>
            
            <div class="endpoint">
                <h3><span class="method method-POST">POST</span>/api/v1/students</h3>
                <p>Create a new student</p>
                <div class="code">curl -X POST http://localhost:8000/api/v1/students \\<br>
  -H "Content-Type: application/json" \\<br>
  -d '{"name": "John Doe", "email": "john@example.com"}'</div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method method-GET">GET</span>/api/v1/students/{id}/progress</h3>
                <p>Get student learning progress</p>
                <div class="code">curl http://localhost:8000/api/v1/students/1/progress</div>
            </div>
            
            <h2>📖 Courses</h2>
            
            <div class="endpoint">
                <h3><span class="method method-POST">POST</span>/api/v1/courses</h3>
                <p>Create a new course</p>
                <div class="code">curl -X POST http://localhost:8000/api/v1/courses \\<br>
  -H "Content-Type: application/json" \\<br>
  -d '{"title": "Python Basics", "description": "Learn Python programming"}'</div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method method-GET">GET</span>/api/v1/courses</h3>
                <p>Get list of all courses</p>
                <div class="code">curl http://localhost:8000/api/v1/courses</div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method method-POST">POST</span>/api/v1/courses/{id}/enroll</h3>
                <p>Enroll student to course</p>
                <div class="code">curl -X POST http://localhost:8000/api/v1/courses/1/enroll \\<br>
  -H "Content-Type: application/json" \\<br>
  -d '{"student_id": 1}'</div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method method-GET">GET</span>/api/v1/courses/{id}/lessons</h3>
                <p>Get course lessons</p>
                <div class="code">curl http://localhost:8000/api/v1/courses/1/lessons</div>
            </div>
            
            <h2>✅ Learning Progress</h2>
            
            <div class="endpoint">
                <h3><span class="method method-POST">POST</span>/api/v1/lessons/{id}/complete</h3>
                <p>Mark lesson as completed</p>
                <div class="code">curl -X POST http://localhost:8000/api/v1/lessons/1/complete \\<br>
  -H "Content-Type: application/json" \\<br>
  -d '{"student_id": 1, "time_spent": 1800}'</div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method method-POST">POST</span>/api/v1/submissions</h3>
                <p>Submit assignment solution</p>
                <div class="code">curl -X POST http://localhost:8000/api/v1/submissions \\<br>
  -H "Content-Type: application/json" \\<br>
  -d '{"student_id": 1, "lesson_id": 1, "content": "My solution code..."}'</div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method method-GET">GET</span>/api/v1/submissions</h3>
                <p>Get submissions list</p>
                <div class="code">curl http://localhost:8000/api/v1/submissions</div>
            </div>
            
            <h2>📊 Analytics (Heavy Queries)</h2>
            
            <div class="endpoint">
                <h3><span class="method method-GET">GET</span>/api/v1/analytics/courses</h3>
                <p>Course analytics (slow endpoint for testing alerts)</p>
                <div class="code">curl http://localhost:8000/api/v1/analytics/courses</div>
            </div>
            
            <h2>📝 Response Examples</h2>
            <h3>Student Object</h3>
            <div class="code">{<br>
  "id": 1,<br>
  "name": "John Doe",<br>
  "email": "john@example.com",<br>
  "created_at": "2023-01-01T12:00:00Z"<br>
}</div>
            
            <h3>Course Object</h3>
            <div class="code">{<br>
  "id": 1,<br>
  "title": "Python Basics",<br>
  "description": "Learn Python programming",<br>
  "created_at": "2023-01-01T12:00:00Z"<br>
}</div>
        </div>
    </div>
</body>
</html>
"""

# Load Testing UI
LOAD_TEST_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LearnTracker Load Testing</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .form-group {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #0056b3;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .status {
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            display: none;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .metrics-link {
            text-align: center;
            margin: 20px 0;
        }
        .metrics-link a {
            color: #007bff;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 LearnTracker Load Testing</h1>
        <p>Use this tool to generate load on the LearnTracker API and test monitoring alerts.</p>
        
        <div class="metrics-link">
            <a href="/metrics" target="_blank">📊 View Current Metrics</a>
        </div>
        
        <form id="loadTestForm">
            <div class="form-group">
                <label for="endpoint">Target Endpoint:</label>
                <select id="endpoint" name="endpoint">
                    <option value="/api/v1/courses">GET /api/v1/courses</option>
                    <option value="/api/v1/analytics/courses">GET /api/v1/analytics/courses (Slow)</option>
                    <option value="/api/v1/submissions">GET /api/v1/submissions</option>
                    <option value="/health">GET /health</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="rps">Requests Per Second (RPS):</label>
                <input type="number" id="rps" name="rps" value="50" min="1" max="500">
            </div>
            
            <div class="form-group">
                <label for="duration">Duration (seconds):</label>
                <input type="number" id="duration" name="duration" value="60" min="10" max="300">
            </div>
            
            <button type="submit" id="startButton">Start Load Test</button>
            <button type="button" id="stopButton" style="display: none; background: #dc3545;">Stop Test</button>
        </form>
        
        <div id="status" class="status"></div>
        
        <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 5px;">
            <h3>💡 Tips for Testing Alerts:</h3>
            <ul>
                <li><strong>p99 Latency Alert:</strong> Use "analytics/courses" endpoint with 100+ RPS</li>
                <li><strong>DB RPS Alert:</strong> Use any endpoint with 150+ RPS for 30+ seconds</li>
                <li><strong>Monitor:</strong> Check Telegram channel and Grafana dashboards</li>
            </ul>
        </div>
    </div>

    <script>
        let loadTestInterval = null;
        let isRunning = false;
        let totalRequests = 0;
        let successfulRequests = 0;

        document.getElementById('loadTestForm').addEventListener('submit', function(e) {
            e.preventDefault();
            startLoadTest();
        });

        document.getElementById('stopButton').addEventListener('click', function() {
            stopLoadTest();
        });

        function startLoadTest() {
            const endpoint = document.getElementById('endpoint').value;
            const rps = parseInt(document.getElementById('rps').value);
            const duration = parseInt(document.getElementById('duration').value);
            
            if (isRunning) return;
            
            isRunning = true;
            totalRequests = 0;
            successfulRequests = 0;
            
            // Update UI
            document.getElementById('startButton').style.display = 'none';
            document.getElementById('stopButton').style.display = 'block';
            showStatus(`Starting load test: ${rps} RPS to ${endpoint} for ${duration} seconds...`, 'info');
            
            // Calculate interval between requests
            const intervalMs = 1000 / rps;
            
            // Start sending requests
            loadTestInterval = setInterval(() => {
                sendRequest(endpoint);
            }, intervalMs);
            
            // Stop after duration
            setTimeout(() => {
                if (isRunning) {
                    stopLoadTest();
                }
            }, duration * 1000);
        }

        function stopLoadTest() {
            if (!isRunning) return;
            
            isRunning = false;
            
            if (loadTestInterval) {
                clearInterval(loadTestInterval);
                loadTestInterval = null;
            }
            
            // Update UI
            document.getElementById('startButton').style.display = 'block';
            document.getElementById('stopButton').style.display = 'none';
            
            const successRate = totalRequests > 0 ? (successfulRequests / totalRequests * 100).toFixed(1) : 0;
            showStatus(`Load test completed. Total: ${totalRequests}, Success: ${successfulRequests} (${successRate}%)`, 'success');
        }

        function sendRequest(endpoint) {
            totalRequests++;
            
            fetch(endpoint)
                .then(response => {
                    if (response.ok) {
                        successfulRequests++;
                    }
                })
                .catch(error => {
                    console.error('Request failed:', error);
                });
            
            // Update status every 50 requests
            if (totalRequests % 50 === 0) {
                const successRate = (successfulRequests / totalRequests * 100).toFixed(1);
                showStatus(`Running... Sent: ${totalRequests}, Success: ${successfulRequests} (${successRate}%)`, 'info');
            }
        }

        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = `status ${type}`;
            status.style.display = 'block';
        }
    </script>
</body>
</html>
"""

# Роутеры

# Главная страница и документация
@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(content=DOCS_HTML)

@app.get("/docs", response_class=HTMLResponse)
async def docs():
    return HTMLResponse(content=DOCS_HTML)

@app.get("/load-test", response_class=HTMLResponse)
async def load_test_ui():
    return HTMLResponse(content=LOAD_TEST_HTML)

# Health check
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Проверяем подключение к БД
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        
        # Обновляем бизнес-метрики
        metrics.update_business_metrics(db)
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "service": "learntracker",
            "database": "postgresql"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

# Метрики
@app.get("/metrics", response_class=PlainTextResponse)
async def get_metrics(db: Session = Depends(get_db)):
    # Обновляем бизнес-метрики перед экспортом
    metrics.update_business_metrics(db)
    return metrics.get_metrics()

# API Endpoints

# Студенты
@app.post("/api/v1/students", response_model=schemas.Student)
@metrics.monitor_db_operation("create_student")
async def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    # Проверяем, не существует ли студент с таким email
    db_student = crud.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Student with this email already exists")
    
    return crud.create_student(db=db, student=student)

@app.get("/api/v1/students/{student_id}/progress", response_model=schemas.StudentProgress)
@metrics.monitor_db_operation("get_student_progress")
async def get_student_progress(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return crud.get_student_progress(db=db, student_id=student_id)

# Курсы
@app.post("/api/v1/courses", response_model=schemas.Course)
@metrics.monitor_db_operation("create_course")
async def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db=db, course=course)

@app.get("/api/v1/courses", response_model=List[schemas.Course])
@metrics.monitor_db_operation("get_courses")
async def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses

@app.get("/api/v1/courses/{course_id}", response_model=schemas.Course)
@metrics.monitor_db_operation("get_course")
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.post("/api/v1/courses/{course_id}/enroll")
@metrics.monitor_db_operation("enroll_student")
async def enroll_student(course_id: int, enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # Проверяем существование курса и студента
    course = crud.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    student = crud.get_student(db, student_id=enrollment.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    result = crud.enroll_student(db=db, course_id=course_id, student_id=enrollment.student_id)
    if result is None:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")
    
    return {"message": "Student enrolled successfully", "enrollment_id": result.id}

@app.get("/api/v1/courses/{course_id}/lessons", response_model=List[schemas.Lesson])
@metrics.monitor_db_operation("get_course_lessons")
async def get_course_lessons(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return crud.get_course_lessons(db=db, course_id=course_id)

# Прохождение уроков
@app.post("/api/v1/lessons/{lesson_id}/complete")
@metrics.monitor_db_operation("complete_lesson")
async def complete_lesson(lesson_id: int, completion: schemas.LessonCompletionCreate, db: Session = Depends(get_db)):
    result = crud.complete_lesson(db=db, lesson_id=lesson_id, completion=completion)
    if result is None:
        raise HTTPException(status_code=400, detail="Lesson already completed by this student")
    
    # Инкрементируем метрику
    metrics.increment_lesson_completion()
    
    return {"message": "Lesson completed successfully", "completion_id": result.id}

# Решения заданий
@app.post("/api/v1/submissions", response_model=schemas.Submission)
@metrics.monitor_db_operation("create_submission")
async def create_submission(submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    result = crud.create_submission(db=db, submission=submission)
    
    # Инкрементируем метрику
    metrics.increment_submission(status="pending")
    
    return result

@app.get("/api/v1/submissions", response_model=List[schemas.Submission])
@metrics.monitor_db_operation("get_submissions")
async def get_submissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_submissions(db=db, skip=skip, limit=limit)

# Аналитика (медленные запросы)
@app.get("/api/v1/analytics/courses", response_model=List[schemas.CourseAnalytics])
@metrics.monitor_db_operation("get_course_analytics")
async def get_course_analytics(db: Session = Depends(get_db)):
    """Медленный эндпоинт для тестирования алертов по латенси"""
    return crud.get_course_analytics(db=db)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)