#!/bin/bash

# Скрипт для запуска LearnTracker через Docker

echo "🐳 Запуск LearnTracker через Docker..."

# Останавливаем существующие контейнеры
echo "🔄 Останавливаем существующие контейнеры..."
docker stop learntracker-app learntracker-db 2>/dev/null || true
docker rm learntracker-app learntracker-db 2>/dev/null || true

# Создаем сеть для контейнеров
echo "🌐 Создаем Docker сеть..."
docker network create learntracker-network 2>/dev/null || true

# Запускаем PostgreSQL
echo "🐘 Запускаем PostgreSQL..."
docker run --name learntracker-db \
    --network learntracker-network \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=learntracker \
    -p 5432:5432 \
    -d postgres:13

# Ждем запуска базы данных
echo "⏳ Ждем запуска базы данных..."
sleep 15

# Собираем образ приложения
echo "🔨 Собираем образ приложения..."
docker build -t learntracker-app .

# Запускаем приложение
echo "🚀 Запускаем приложение..."
docker run --name learntracker-app \
    --network learntracker-network \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_HOST=learntracker-db \
    -e POSTGRES_PORT=5432 \
    -e POSTGRES_DB=learntracker \
    -p 8000:8000 \
    -d learntracker-app

echo "✅ LearnTracker запущен на http://localhost:8000"
echo "📊 Метрики доступны на http://localhost:8000/metrics"
echo "🔧 Нагрузочное тестирование: http://localhost:8000/load-test"

