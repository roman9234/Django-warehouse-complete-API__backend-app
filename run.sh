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

# Создаём БД если её ещё нет
echo "Attempting to create database $POSTGRES_DB..."
if ! psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1; then
  psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $POSTGRES_DB;"
  echo "Database $POSTGRES_DB created"
else
  echo "Database $POSTGRES_DB already exists"
fi

# Создаём пользователя если его нет
echo "Attempting to create user postgres..."
if ! psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -tc "SELECT 1 FROM pg_user WHERE usename = 'postgres'" | grep -q 1; then
  psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -c "CREATE USER postgres WITH PASSWORD 'postgres';"
  echo "User postgres created"
else
  echo "User postgres already exists"
fi

# Даём права пользователю на БД
echo "Granting privileges..."
psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO postgres;"
echo "Privileges granted"

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate --noinput
echo "migrated"

# Создаём суперпользователя (только если его нет)
#echo "Creating superuser..."
#DJANGO_SUPERUSER_USERNAME="admin" \
#DJANGO_SUPERUSER_PASSWORD="admin" \
#DJANGO_SUPERUSER_EMAIL="admin@example.com" \
#python manage.py createsuperuser --noinput || echo "Superuser already exists or error occurred"

# Запуск приложения
echo "Starting server..."
python manage.py runserver --noreload 0.0.0.0:8000
