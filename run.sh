#!/usr/bin/env sh

#Применяем миграции
#--noinput для того чтобы не запрашивался ввод пользователя
python manage.py migrate --noinput

#Создаём суперпользователя
#Выставлем переменные окружения для этой команды
DJANGO_SUPERUSER_USERNAME="admin" \
  DJANGO_SUPERUSER_PASSWORD="admin" \
  DJANGO_SUPERUSER_EMAIL="admin@example.com"\
  python manage.py createsuperuser --noinput

#Запуск приложения
#noreload чтобы Django не отслеживал изменения файлов в проекте для перезапуска
python manage.py runserver --noreload 0.0.0.0:8000





