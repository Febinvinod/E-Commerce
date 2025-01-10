from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # Make user optional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField(null=True)  # Assuming product IDs are integers
    quantity = models.PositiveIntegerField(default=1)
    visible = models.BooleanField(default=True)
    


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses", null=True, blank=True)
    street = models.TextField(null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)  # Mark as default address

class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery_days = models.IntegerField(null=True)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name="order")
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
