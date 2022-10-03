from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from . import serializers, models


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """

    queryset = get_user_model().objects.all().order_by("role")
    serializer_class = serializers.UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint that allows products to be viewed or edited"""

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint that allows orders to be viewed or edited"""

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    """API endpoint that allows an order item to be viewed or edited"""

    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """API endpoint that allows address to be viewed or edited"""

    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows approved to be viewed"""

    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer


class RefundViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows approved refund to be viewed"""

    queryset = models.Refund.objects.all()
    serializer_class = serializers.RefundSerializer


class CouponViewSet(viewsets.ModelViewSet):
    """API endpoint that allows coupons to be edited and viewed"""

    queryset = models.Coupon.objects.all()
    serializer_class = serializers.CouponSerializer
