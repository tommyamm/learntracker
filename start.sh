#!/bin/bash

VENV_DIR="learntrackervenv"

echo "🚀 Запуск LearnTracker..."

# Проверяем, установлен ли Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Проверяем, запущен ли Docker daemon
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon не запущен. Запускаем Docker..."
    sudo systemctl start docker
fi

# Останавливаем существующий контейнер, если он запущен
echo "🔄 Останавливаем существующий контейнер базы данных..."
docker stop learntracker-db 2>/dev/null || true
docker rm learntracker-db 2>/dev/null || true

# Запускаем PostgreSQL контейнер
echo "🐘 Запускаем PostgreSQL..."
docker run --name learntracker-db \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=learntracker \
    -p 5432:5432 \
    -d postgres:13

# Ждем, пока база данных запустится
echo "⏳ Ждем запуска базы данных..."
sleep 10

# Проверяем наличие pip
echo "🧰 Проверяем pip..."
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip не установлен. Устанавливаем..."
    python3 -m ensurepip --upgrade || {
        echo "❌ Не удалось установить pip!"
        exit 1
    }
fi

# Проверяем наличие venv модуля
echo "🧰 Проверяем модуль venv..."
if ! python3 -m venv --help &> /dev/null; then
    echo "❌ Модуль venv не установлен. Устанавливаем..."
    sudo apt-get update && sudo apt-get install -y python3-venv || {
        echo "❌ Не удалось установить python3-venv!"
        exit 1
    }
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "🛠 Создание виртуального окружения..."
    python3 -m venv "$VENV_DIR"
fi

if [ -z "$VIRTUAL_ENV" ]; then
    echo "🔁 Активация виртуального окружения..."
    source "$VENV_DIR/bin/activate"
else
    echo "✅ Виртуальное окружение уже активировано: $VIRTUAL_ENV"
fi

if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Ошибка активации виртуального окружения!"
    exit 1
fi

# Устанавливаем переменные окружения
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=learntracker

# Устанавливаем зависимости Python
pip install -r requirements.txt

# Запускаем приложение
echo "🌐 Запускаем веб-приложение на http://localhost:8000"
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload