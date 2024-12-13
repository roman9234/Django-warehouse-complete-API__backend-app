from rest_framework import serializers
from rest_framework import validators


from api.models import ApiUser, Warehouse, Product, Request

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUser
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}



