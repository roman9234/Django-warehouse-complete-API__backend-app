from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import ApiUser, Warehouse, Product, Request
from api.permissions import IsNotAuthenticated, IsNotAuthenticatedOrAdmin, IsRequesterOrAdmin, IsSupplierOrAdmin, \
    IsSupplierOfProduct, IsRequesterOfProduct

from api.serializers import UserSerializer, WarehouseSerializer, ProductSerializer, RequestSerializer

from django.http import HttpResponseForbidden


# Create your views here.


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer

    http_method_names = ["post", "get", "put", "delete"]


    # create, list, retrieve, update, partial_update, destroy
    def get_permissions(self):
        if self.action == 'list':  # Доступ ко всем данным
            permission_classes = [AllowAny]
        elif self.action in ['create']:
            permission_classes = [IsNotAuthenticatedOrAdmin]
        elif self.action in ['retrieve', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]





class WarehouseModelViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    @action(detail=True)
    def requests(self, request, pk=None):
        warehouse = get_object_or_404(Warehouse.objects.all(), id=pk)
        requests = warehouse.requests
        return Response(
            RequestSerializer(requests, many=True).data
        )

    http_method_names = ["post", "get", "put", "delete"]

    # create, list, retrieve, update, partial_update, destroy
    def get_permissions(self):
        if self.action == 'list':  # Доступ ко всем данным
            permission_classes = [AllowAny]
        elif self.action in ['create']:
            permission_classes = [IsAdminUser]
        elif self.action in ['retrieve', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]





class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True)
    def requests(self, request, pk=None):
        product = get_object_or_404(Product.objects.all(), id=pk)
        requests = product.requests
        return Response(
            RequestSerializer(requests, many=True).data
        )

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Доступ ко всем данным
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsSupplierOrAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsSupplierOfProduct | IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Установить текущего пользователя как customer (заказчик)
        if self.request.user.is_supplier:
            serializer.save(producer=self.request.user)
        else:
            raise PermissionDenied("Только производители могут создавать продукты.")


# TODO узнать можно ли натсроить форму в API ROOT так, чтобы вместо ID там отображались названия
class RequestModelViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    http_method_names = ["post", "get", "put", "delete"]

    # create, list, retrieve, update, partial_update, destroy
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Доступ ко всем данным
            permission_classes = [AllowAny]
        elif self.action in ['create']:
            permission_classes = [IsRequesterOrAdmin]
        elif self.action in ['update', 'partial_update']:
            # или поставщик продукта или заказчик продукта
            permission_classes = [IsSupplierOfProduct | IsRequesterOfProduct | IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Установить текущего пользователя как customer (заказчик)
        if not self.request.user.is_supplier:
            serializer.save(customer=self.request.user, request_supplied=False, request_retrieved=False)
        else:
            raise PermissionDenied("Только заказчики могут создавать заявки.")

    # TODO проверить все варианты поведения
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Проверяем права на изменение полей
        if 'request_supplied' in request.data:
            if instance.request_supplied and request.data['request_supplied'] == "true":
                pass
            else:
                if instance.product.producer != request.user:
                    raise PermissionDenied("Только поставщик может изменить статус доставки.")

        if 'request_retrieved' in request.data:
            if instance.customer != request.user:
                raise PermissionDenied("Только заказчик может изменить статус получения.")
            if not instance.request_supplied:
                raise PermissionDenied("Товар ещё не доставлен поставщиком.")

        return super().update(request, *args, **kwargs)
