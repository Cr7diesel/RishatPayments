from rest_framework import serializers

from .models import User, Item, Order, Discount, Tax


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email")
        read_only_fields = ("id",)


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = "__all__"

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    items = ItemSerializer(read_only=True, many=True)
    discount = serializers.IntegerField(source="discount.percent")
    tax = serializers.DecimalField(
        source="tax.tax_rate", max_digits=3, decimal_places=1
    )

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            instance.save()
        return instance


class DiscountSerializer(serializers.ModelSerializer):

    order = OrderSerializer(read_only=True)

    class Meta:
        model = Discount
        fields = "__all__"


class TaxSerializer(serializers.ModelSerializer):

    order = OrderSerializer(read_only=True)

    class Meta:
        model = Tax
        fields = "__all__"
