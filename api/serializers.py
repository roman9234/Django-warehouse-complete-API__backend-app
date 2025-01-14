from rest_framework import serializers
from rest_framework import validators


from api.models import ApiUser, Warehouse, Product, Request

class UserSerializer(serializers.Serializer):
    # Также добавим валидацию уникальности - username должен быть уникальным
    username = serializers.CharField(max_length=128, validators=[
        # Проверяем нет ли уже такого username используя встроенный в validators валидатор
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    # у serializers есть специальное поле для Email
    email = serializers.EmailField(validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    # Тут лучше было бы настроить валидацию пароля
    # write_only=True не позволяет отправить пароль в открытом виде клиенту после регистрации
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)

    is_supplier = serializers.BooleanField()

    def update(self, instance, validated_data):
        # username не обновляется
        # is_supplier не обновляется
        if email := validated_data.get("email"):
            instance.email = email
            instance.save(update_fields=["email"])

        if password := validated_data.get("password"):
            instance.set_password(password)
            instance.save(update_fields=["password"])
        return instance

    def create(self, validated_data):
        # Простая логика:
        user = ApiUser.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            is_supplier=validated_data["is_supplier"]
        )
        # Так как пароль хранится в зашифрованном виде, для его задания нужно использовать метод set_password
        user.set_password(validated_data["password"])
        # Сохраняем изменения. Пишем что обновили только одно поле, так как остальные были изменены при создании
        user.save(update_fields=["password"])
        return user

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "producer": {"read_only": True},
        }

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
        # TODO узнать можно ли настроить разные read_only для создания и обновления
        extra_kwargs = {
            "id": {"read_only": True},
            # "request_supplied": {"read_only": True},  # Это поле обновляется только поставщиком
            # "request_retrieved": {"read_only": True},  # Это поле обновляется только заказчиком
            "customer": {"read_only": True},
        }

    # Кастомный валидатор
    def validate(self, attrs):
        request = self.context['request']
        user = request.user

        # только заказчик может создавать заявку
        if request.method == "POST" and user.is_supplier:
            raise serializers.ValidationError("Только заказчики могут создавать заявки.")

        # заказчик может установить request_retrieved=True только если request_supplied=True
        if 'request_retrieved' in attrs and attrs['request_retrieved']:
            # текущий объект (если это update)
            instance = self.instance
            if not instance or not instance.request_supplied:
                raise serializers.ValidationError("Товар ещё не доставлен поставщиком.")

        return attrs




