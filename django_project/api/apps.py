"""
Неиспользуемый файл
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Неиспользуемый класс
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Перенесите код, работающий с моделями, в сигналы или отложите выполнение
        from django.db.models.signals import post_migrate
        from .signals import setup_admin_user  # Ваш обработчик

        post_migrate.connect(setup_admin_user, sender=self)
