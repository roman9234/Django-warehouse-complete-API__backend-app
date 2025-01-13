from django.contrib.auth.models import AbstractUser
from django.db import models



class ApiUser(AbstractUser):
    is_supplier = models.BooleanField(default=False)


# Наследуем от модели
class Warehouse(models.Model):
    name = models.CharField(max_length=128)


class Product(models.Model):
    name = models.CharField(max_length=128)

# Только Requester может создавать поля requests и редактировать поле request_retrieved
# Только supplier может редактировать поле request_supplied
# Создание request -> заказ доставляется (request_supplied) -> заказ забирается заказчиком (request_retrieved)

class Request(models.Model):
    product = models.ForeignKey(Product, related_name="requests", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    warehouse = models.ForeignKey(Warehouse, related_name="requests", on_delete=models.CASCADE)
    supplier = models.ForeignKey(ApiUser, related_name="requests", on_delete=models.CASCADE)
    request_supplied = models.BooleanField(default=False)
    request_retrieved = models.BooleanField(default=False)
    # TODO поле customer
    # customer = models.ForeignKey(ApiUser, related_name="customer_requests", on_delete=models.CASCADE)


