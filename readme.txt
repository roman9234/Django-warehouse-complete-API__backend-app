---- Запсук сервера ----


Для запуска сервера Django необходимо выполнить команду
python manage.py runserver
Это запустит локальный сервер на порту по умолчанию (обычно 8000)


---- работа с pip-tools ----
Устанавливаем зависимости по файлу requirements.in:


pip install pip-tools
pip-compile.exe
pip-sync.exe


---- Создаём проект ----
django-admin startproject logistics


создать приложение с названием api
python manage.py startapp api

Добавляем всё в installed_apps

Создаём модели

Изменяем settings.py:

AUTH_USER_MODEL = 'api.ApiUser'
REST_FRAMEWORK = {...}

исполняем миграции
python manage.py makemigrations
python manage.py migrate


---- Создание суперпользователя для отладки ----
python manage.py createsuperuser --username=superuser --email=superuser@mail.ru












