from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "role",
            "first_name",
            "last_name",
            "is_anonymous",
            "is_authenticated",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        exclude = ["slug", "image"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = "__all__"


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Refund
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon
        fields = "__all__"
