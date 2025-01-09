from django.db import models

class OrderStatus(models.Model):
    # Referencing the Order model by string to avoid circular imports
    order = models.OneToOneField(
        'kartx_cart.Order',  # Use the string format to reference the model
        on_delete=models.CASCADE,
        related_name="status"
    )
    status = models.CharField(max_length=20, choices=[
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='processing')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order.id} - {self.status}"
