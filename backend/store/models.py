from unicodedata import name
from uuid import uuid4
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """Creates, saves and returns a User"""
        if not email:
            raise ValueError(_("User must have an email"))

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and save a superuser with the given email and password"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # removing the username field
    username = None

    # creating the roles class
    class Role(models.TextChoices):
        STAFF = "STAFF", "Staff"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(
        _("Roles"),
        max_length=50,
        choices=Role.choices,
        default=Role.CUSTOMER,
        editable=True,
    )

    # Set the email field as the username field instead of an actual username
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Setting the manager for creating the user
    objects = UserManager()

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(_("first name"), max_length=90, blank=False)
    last_name = models.CharField(_("last name"), max_length=90)
    is_anonymous = models.BooleanField(default=True)
    is_authenticated = models.BooleanField(default=False)


class StaffManager(models.Manager):
    """The queryset and functions for staff models"""

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.STAFF)


class CustomerManager(models.Manager):
    """The queryset and other functions for the customer models"""

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.CUSTOMER)


class Product(models.Model):
    # The different types of shirts
    class Category(models.TextChoices):
        SHORT = "SHORT", "Short Sleeves"
        LONG = "LONG", "Long Sleeves"
        HOODIE = "HOODIE", "Hoodie"

    #  The sizes of the clothes
    class Size(models.TextChoices):
        XS = "XS", "Extra Small"
        S = "S", "Small"
        M = "M", "Medium"
        L = "L", "Large"
        XL = "XL", "Extra Large"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=Category.choices, max_length=30)
    size = models.CharField(choices=Size.choices, max_length=5)
    description = models.TextField(_("Cloth description"))
    quantity = models.IntegerField()
    image = models.ImageField(blank=True)
    slug = models.SlugField(blank=True)


class Staff(User):
    objects = StaffManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.role = User.Role.STAFF
        return super().save(*args, **kwargs)


class Customer(User):
    objects = CustomerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.role = User.Role.CUSTOMER
        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    """A product that has been ordered"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def total_price(self):
        return self.quantity * self.item.price

    def get_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.total_price() - self.get_discount_price()

    def final_price(self):
        if self.item.discount_price:
            return self.get_discount_price()
        return self.total_price()


class Order(models.Model):
    """The whole order a user has made"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    shipping_address = models.ForeignKey(
        "Address",
        related_name=_("shipping_address"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    billing_address = models.ForeignKey(
        "Address",
        related_name=_("billing_address"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    payment = models.ForeignKey(
        "Payment", on_delete=models.SET_NULL, blank=True, null=True
    )
    coupon = models.ForeignKey(
        "Coupon", on_delete=models.SET_NULL, blank=True, null=True
    )
    being_delivered = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def total_price(self):
        """gets the total price of the items ordered"""
        total = 0
        for order_item in self.items.all():
            total += order_item.total_price
        return total


class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    street_address = models.CharField(max_length=150)
    apartment_address = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"


class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True
    )
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Refund(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
