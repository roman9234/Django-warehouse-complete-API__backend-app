#!/usr/bin/env sh

# Функция для проверки доступности PostgreSQL
wait_for_postgres() {
  until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' >/dev/null 2>&1; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
  done
  echo "PostgreSQL is up - continuing"
}

# Автоматически создаём БД если её ещё нет
psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB;" || echo "Database already exists"
echo "created DB"
docker-compose exec app-postgres psql -U postgres -c "CREATE USER postgres WITH PASSWORD 'postgres';"
echo "created user"
docker-compose exec app-postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE django_app TO postgres;"
echo "created user"

# Ждём, пока PostgreSQL станет доступен
export PGPASSWORD="$POSTGRES_PASSWORD"
wait_for_postgres
echo "waited"

# Применяем миграции
python manage.py migrate --noinput
echo "migrated"

# Создаём суперпользователя (только если его нет)
#DJANGO_SUPERUSER_USERNAME="admin" \
#DJANGO_SUPERUSER_PASSWORD="admin" \
#DJANGO_SUPERUSER_EMAIL="admin@example.com" \
#python manage.py createsuperuser --noinput || echo "Superuser already exists or error occurred"

# Запуск приложения
python manage.py runserver --noreload 0.0.0.0:8000
