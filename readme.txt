


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

исполняем миграции
python manage.py makemigrations


---- Запсук сервера----


Для запуска сервера Django необходимо выполнить команду
python manage.py runserver
Это запустит локальный сервер на порту по умолчанию (обычно 8000)


TODO сделать регистрацию
TODO сделать указание типа поставщик/потребитель
TODO сделать аутентификацию

TODO сделать для каждого товара привязку к поставщику

TODO создавать склады и товары могут только поставщики
TODO сделать доступ только к некоторым полям для поставщиков и потребителей: поставщик создаёт отправления на склад и указывает, прибыло ли оно. Потребитель может указать, забрал ли он его
либо понять как можно сделать по другому



---- ошибка ----


It is impossible to add a non-nullable field 'customer' to request without specifying a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.











