


Устанавливаем зависимости по файлу requirements.in


pip install pip-tools
pip-compile.exe
pip-sync.exe


Создаём проект
django-admin startproject logistics


создать приложение с названием api
python manage.py startapp api

Добавляем всё в installed_apps

Создаём модели

Изменяем settings.py:

AUTH_USER_MODEL = 'api.ApiUser'
REST_FRAMEWORK = {...}


python manage.py makemigrations






It is impossible to add a non-nullable field 'customer' to request without specifying a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.











