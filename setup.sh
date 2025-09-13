#!/bin/bash

# Скрипт для налаштування середовища Apache Airflow

echo "🚀 Налаштування Apache Airflow для Olympic Medal Processing DAG"

# Створення необхідних директорій
echo "📁 Створення директорій..."
mkdir -p logs plugins

# Встановлення прав доступу
echo "🔐 Встановлення прав доступу..."
chmod +x setup.sh

# Копіювання файлу конфігурації
if [ ! -f .env ]; then
    echo "📋 Створення файлу конфігурації..."
    cp .env.example .env
    echo "⚠️  Будь ласка, відредагуйте файл .env за потреби"
fi

# Ініціалізація бази даних Airflow
echo "🗄️  Ініціалізація бази даних..."
docker-compose up airflow-init

echo "✅ Налаштування завершено!"
echo ""
echo "🎯 Для запуску Airflow виконайте:"
echo "   docker-compose up -d"
echo ""
echo "🌐 Веб-інтерфейс буде доступний за адресою:"
echo "   http://localhost:8080"
echo "   Логін: admin"
echo "   Пароль: admin"
echo ""
echo "📊 MySQL буде доступний на порту 3306"
echo "   Хост: localhost"
echo "   Користувач: airflow"
echo "   Пароль: airflow"