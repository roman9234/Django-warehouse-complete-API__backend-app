"""
Модуль содержащий модели ORM
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

# (Админы имеют доступ ко всем действиям)

# Только неавторизованные пользователи могут создавать аккаунты
class ApiUser(AbstractUser):
    """
    Переопределённая модель пользователя
    """
    is_supplier = models.BooleanField(default=False)


# Только админы могут создавать склады
class Warehouse(models.Model):
    """
    Модель склада
    """
    name = models.CharField(max_length=128)

# Только Suppliers могут создавать продукты
class Product(models.Model):
    """
    Модель продукта
    """
    name = models.CharField(max_length=128)
    producer = models.ForeignKey(
        ApiUser,
        related_name="producer_products",
        on_delete=models.CASCADE,
        default=None
    )


# Только Requester может создавать поля requests и редактировать поле request_retrieved
# Только supplier может редактировать поле request_supplied
# Создание request -> заказ доставляется (request_supplied) -> заказ забирается заказчиком
# (request_retrieved)

class Request(models.Model):
    """
    Модель запроса
    """
    product = models.ForeignKey(Product, related_name="requests", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    warehouse = models.ForeignKey(Warehouse, related_name="requests", on_delete=models.CASCADE)
    request_supplied = models.BooleanField(default=False)
    request_retrieved = models.BooleanField(default=False)
    customer = models.ForeignKey(
        ApiUser,
        related_name="customer_requests",
        on_delete=models.CASCADE,
        default=None
    )
