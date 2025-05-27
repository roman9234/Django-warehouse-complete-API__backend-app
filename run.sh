#!/usr/bin/env sh

# Установка пароля для psql
export PGPASSWORD="$POSTGRES_PASSWORD"

# Функция для проверки доступности PostgreSQL
wait_for_postgres() {
  until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -c "SELECT 1;" >/dev/null 2>&1; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 2
  done
  echo "PostgreSQL is up - continuing"
}

# Ждём, пока PostgreSQL станет доступен
wait_for_postgres

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate --noinput

#python manage.py showmigrations --skip-checks

#Собираем статические файлы
echo "Collecting static files..."
mkdir static/
python manage.py collectstatic --noinput

# Запуск приложения
echo "Starting server..."
python manage.py runserver --noreload 0.0.0.0:8000
