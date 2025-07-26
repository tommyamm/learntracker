# LearnTracker - Образовательная платформа для отслеживания прогресса обучения

LearnTracker - это веб-приложение на базе FastAPI для управления образовательными курсами, студентами и отслеживания прогресса обучения.

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.11+
- Docker
- pip

### Установка и запуск

1. **Клонируйте или распакуйте проект:**
   ```bash
   # Если у вас есть архив
   tar -xzf learntracker.tar.gz
   cd learntracker
   ```

2. **Запустите приложение:**
   ```bash
   ./start.sh
   ```

3. **Откройте браузер и перейдите по адресу:**
   ```
   http://localhost:8000
   ```

### Остановка приложения

```bash
./stop.sh
```

## 📋 Функциональность

### Основные возможности:
- 👨‍🎓 Управление студентами
- 📚 Управление курсами и уроками
- ✅ Отслеживание прогресса обучения
- 📝 Система заданий и решений
- 📊 Аналитика и метрики
- 🔧 Инструменты для нагрузочного тестирования

### API Endpoints:

#### Здоровье системы
- `GET /health` - Проверка состояния приложения
- `GET /metrics` - Метрики Prometheus

#### Студенты
- `POST /api/v1/students` - Создать студента
- `GET /api/v1/students/{id}/progress` - Получить прогресс студента

#### Курсы
- `POST /api/v1/courses` - Создать курс
- `GET /api/v1/courses` - Получить список курсов
- `GET /api/v1/courses/{id}` - Получить курс по ID
- `POST /api/v1/courses/{id}/enroll` - Записать студента на курс
- `GET /api/v1/courses/{id}/lessons` - Получить уроки курса

#### Обучение
- `POST /api/v1/lessons/{id}/complete` - Отметить урок как завершенный
- `POST /api/v1/submissions` - Отправить решение задания
- `GET /api/v1/submissions` - Получить список решений

#### Аналитика
- `GET /api/v1/analytics/courses` - Аналитика по курсам

## 🛠 Техническая информация

### Архитектура
- **Backend:** FastAPI (Python)
- **База данных:** PostgreSQL
- **ORM:** SQLAlchemy
- **Контейнеризация:** Docker
- **Мониторинг:** Prometheus metrics

### Структура проекта
```
learntracker/
├── app/
│   ├── __init__.py
│   ├── main.py          # Основное приложение FastAPI
│   ├── database.py      # Настройки базы данных
│   ├── models.py        # Модели SQLAlchemy
│   ├── schemas.py       # Pydantic схемы
│   ├── crud.py          # CRUD операции
│   └── metrics.py       # Метрики Prometheus
├── requirements.txt     # Python зависимости
├── docker-compose.yml   # Docker Compose конфигурация
├── start.sh            # Скрипт запуска
├── stop.sh             # Скрипт остановки
└── README.md           # Документация
```

### Переменные окружения
- `POSTGRES_USER` - Пользователь PostgreSQL (по умолчанию: postgres)
- `POSTGRES_PASSWORD` - Пароль PostgreSQL (по умолчанию: postgres)
- `POSTGRES_HOST` - Хост PostgreSQL (по умолчанию: localhost)
- `POSTGRES_PORT` - Порт PostgreSQL (по умолчанию: 5432)
- `POSTGRES_DB` - Имя базы данных (по умолчанию: learntracker)

## 🧪 Тестирование

### Нагрузочное тестирование
Приложение включает встроенный инструмент для нагрузочного тестирования:

1. Откройте http://localhost:8000/load-test
2. Выберите endpoint для тестирования
3. Настройте параметры нагрузки (RPS, длительность)
4. Запустите тест
5. Мониторьте метрики на http://localhost:8000/metrics

### Примеры API запросов

#### Создание студента
```bash
curl -X POST http://localhost:8000/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Иван Иванов", "email": "ivan@example.com"}'
```

#### Создание курса
```bash
curl -X POST http://localhost:8000/api/v1/courses \
  -H "Content-Type: application/json" \
  -d '{"title": "Основы Python", "description": "Изучение основ программирования на Python"}'
```

#### Запись на курс
```bash
curl -X POST http://localhost:8000/api/v1/courses/1/enroll \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1}'
```

## 🔧 Разработка

### Запуск в режиме разработки
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск PostgreSQL
docker run --name learntracker-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=learntracker \
  -p 5432:5432 -d postgres:13

# Установка переменных окружения
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=learntracker

# Запуск приложения с автоперезагрузкой
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Добавление новых зависимостей
```bash
pip install новая_библиотека
pip freeze > requirements.txt
```

## 📊 Мониторинг

Приложение экспортирует метрики в формате Prometheus:
- HTTP запросы (количество, латентность)
- Операции с базой данных
- Бизнес-метрики (студенты, курсы, завершенные уроки)

Метрики доступны по адресу: http://localhost:8000/metrics

## 🐛 Устранение неполадок

### Проблемы с Docker
```bash
# Проверить статус Docker
sudo systemctl status docker

# Запустить Docker
sudo systemctl start docker

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker
```

### Проблемы с базой данных
```bash
# Проверить логи контейнера
docker logs learntracker-db

# Перезапустить контейнер
docker restart learntracker-db

# Подключиться к базе данных
docker exec -it learntracker-db psql -U postgres -d learntracker
```

### Проблемы с Python зависимостями
```bash
# Переустановить зависимости
pip install --force-reinstall -r requirements.txt

# Проверить версию Python
python3 --version
```

## 📝 Лицензия

Этот проект создан в образовательных целях.

## 🤝 Поддержка

При возникновении проблем:
1. Проверьте логи приложения
2. Убедитесь, что Docker запущен
3. Проверьте доступность порта 8000
4. Убедитесь, что все зависимости установлены

