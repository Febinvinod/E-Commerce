from django.db import models
from django.contrib.auth.models import User


class RazorpayOrder(models.Model):
    cart = models.OneToOneField('kartx_cart.Cart', on_delete=models.CASCADE)  # One order per cart
    order_id = models.CharField(max_length=255, unique=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=50, default="created")  # "paid" or "created"

    def __str__(self):
        return f"Razorpay Order: {self.order_id} for Cart #{self.cart.id}"