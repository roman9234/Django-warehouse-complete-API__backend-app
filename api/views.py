from django.shortcuts import render
from rest_framework import viewsets

from api.models import ApiUser, Warehouse, Product, Request
from api.serializers import UserSerializer, WarehouseSerializer, ProductSerializer, RequestSerializer


# Create your views here.


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer


class WarehouseModelViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RequestModelViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer