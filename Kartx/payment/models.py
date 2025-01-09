from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts", null=True, blank=True)  # Make user optional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        """Calculate total price for all items in the cart."""
        total = sum(item.get_total_price() for item in self.items.all())
        return total

    def __str__(self):
        return f"Cart #{self.id}"  # Updated to not depend on the user

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        """Calculate total price for this cart item."""
        return self.quantity * self.price_per_unit

    def __str__(self):
        return f"{self.quantity} x {self.product_name} (Cart #{self.cart.id})"
class RazorpayOrder(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)  # One order per cart
    order_id = models.CharField(max_length=255, unique=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=50, default="created")  # "paid" or "created"

    def __str__(self):
        return f"Razorpay Order: {self.order_id} for Cart #{self.cart.id}"