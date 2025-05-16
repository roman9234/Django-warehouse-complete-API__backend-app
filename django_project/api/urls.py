"""
URL приложения
"""
from rest_framework.routers import DefaultRouter
from django_project.api.views import (
    UserModelViewSet,
    WarehouseModelViewSet,
    ProductModelViewSet,
    RequestModelViewSet
)

router = DefaultRouter()

router.register('users', UserModelViewSet)
router.register('warehouses', WarehouseModelViewSet)
router.register('products', ProductModelViewSet)
router.register('requests', RequestModelViewSet)


urlpatterns = [

]

urlpatterns.extend(router.urls)
