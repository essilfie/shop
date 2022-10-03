from django.contrib import admin
from django.contrib.auth import get_user_model
from . import models

admin.site.register(get_user_model())
admin.site.register(models.Address)
admin.site.register(models.Coupon)
admin.site.register(models.Payment)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Refund)
admin.site.register(models.Product)
admin.site.register(models.Staff)
admin.site.register(models.Customer)
