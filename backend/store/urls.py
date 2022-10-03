from email.mime import base
from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = []

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")
router.register(r"product", views.ProductViewSet, basename="products")
router.register(r"order", views.OrderViewSet, basename="order")
router.register(r"orderitem", views.OrderItemViewSet, basename="orderitem")
router.register(r"address", views.AddressViewSet, basename="address")
router.register(r"payment", views.PaymentViewSet, basename="payment")
router.register(r"refund", views.RefundViewSet, basename="refund")
router.register(r"coupon", views.CouponViewSet, basename="coupon")

urlpatterns += router.urls
