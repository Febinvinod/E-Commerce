from django.db import models
from kartx_cart.models import Cart
class RazorpayOrder(models.Model):
    class PaymentStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        PAID = 'paid', 'Paid'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    # Reference to the Cart model from the kartx_cart app
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)  # One order per cart
    order_id = models.CharField(max_length=255, unique=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(
        max_length=50,
        choices=PaymentStatus.choices,
        default=PaymentStatus.CREATED
    )
    payment_date = models.DateTimeField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Razorpay Order: {self.order_id} for Cart #{self.cart.id}"
  