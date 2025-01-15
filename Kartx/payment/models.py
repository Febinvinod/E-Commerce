from django.db import models


class RazorpayOrder(models.Model):
    cart = models.OneToOneField('kartx_cart.Cart', on_delete=models.CASCADE)  # One order per cart
    order_id = models.CharField(max_length=255, unique=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(
        max_length=50,
        choices=PaymentStatus.choices,
        default=PaymentStatus.CREATED
    )
    payment_date = models.DateTimeField(blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Razorpay Order: {self.order_id} for Cart #{self.cart.id}"
