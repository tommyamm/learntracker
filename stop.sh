#!/bin/bash

# Скрипт для остановки LearnTracker

echo "🛑 Остановка LearnTracker..."

# Останавливаем контейнер PostgreSQL
echo "🐘 Останавливаем PostgreSQL..."
docker stop learntracker-db 2>/dev/null || true
docker rm learntracker-db 2>/dev/null || true

# Останавливаем приложение Python (если запущено в фоне)
echo "🐍 Останавливаем Python приложение..."
pkill -f "uvicorn app.main:app" 2>/dev/null || true

echo "✅ LearnTracker остановлен"

