from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from rest_framework.generics import get_object_or_404

from api.models import ApiUser
# Здесь будем управлять разрешениями permissions

# Создаем пользователя
if not ApiUser.objects.filter(username="admin_user").exists():
    user = ApiUser.objects.create_user(
        username='admin_user',
        email='admin@example.com',
        password='qwerty123'
    )

    # Устанавливаем флаг is_staff=True
    user.is_staff = True
    user.save()



# Создаем группу
group, created = Group.objects.get_or_create(name="Suppliers")

# Назначаем разрешения группе
permissions = Permission.objects.filter(codename__in=[
    "add_product",
    "change_product",
    "delete_product",
])
group.permissions.add(*permissions)


