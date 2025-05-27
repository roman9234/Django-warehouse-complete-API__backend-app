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
        # Этот код выполнится ТОЛЬКО после полной загрузки Django
        # и после применения миграций
        # import api.signals  # Если используете сигналы
        print("API AppConfig.ready() выполнен")
