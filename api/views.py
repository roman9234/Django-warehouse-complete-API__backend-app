from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import ApiUser, Warehouse, Product, Request
from api.permissions import IsNotAuthenticated, IsNotAuthenticatedOrAdmin, IsRequesterOrAdmin, IsSupplierOrAdmin

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
        if self.action == 'list':  # Доступ ко всем данным
            permission_classes = [AllowAny]
        elif self.action in ['create']:
            permission_classes = [IsSupplierOrAdmin]
        elif self.action in ['retrieve', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]



class RequestModelViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    http_method_names = ["post", "get", "put", "delete"]

    # create, list, retrieve, update, partial_update, destroy
    def get_permissions(self):
        if self.action == 'list':  # Доступ ко всем данным
            permission_classes = [AllowAny]
        elif self.action in ['create']:
            permission_classes = [IsRequesterOrAdmin]
        elif self.action in ['retrieve', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

