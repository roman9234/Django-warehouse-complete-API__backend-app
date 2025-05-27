from django.apps import AppConfig
from django.db.utils import ProgrammingError, OperationalError

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Импортируем здесь, чтобы избежать циклических импортов
        from django.contrib.auth.models import Group, Permission
        from api.models import ApiUser

        try:
            # Проверяем, применены ли миграции
            if not ApiUser._meta.db_table:
                return

            # Создаем пользователя, если его нет
            if not ApiUser.objects.filter(username="admin_user").exists():
                user = ApiUser.objects.create_user(
                    username='admin_user',
                    email='admin@example.com',
                    password='qwerty123',
                    is_staff=True
                )
                print("Создан административный пользователь")

            # Создаем группу, если её нет
            group, created = Group.objects.get_or_create(name="Suppliers")
            if created:
                permissions = Permission.objects.filter(codename__in=[
                    "add_product",
                    "change_product",
                    "delete_product",
                ])
                group.permissions.add(*permissions)
                print("Создана группа Suppliers с разрешениями")

        except (ProgrammingError, OperationalError):
            # Игнорируем ошибки, если таблицы ещё не созданы
            pass