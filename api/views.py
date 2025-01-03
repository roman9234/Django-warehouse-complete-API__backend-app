from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.models import ApiUser, Warehouse, Product, Request
from api.serializers import UserSerializer, WarehouseSerializer, ProductSerializer, RequestSerializer


# Create your views here.


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer


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


class RequestModelViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer