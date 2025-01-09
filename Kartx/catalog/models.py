from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    vendor_id = models.IntegerField()  # Placeholder for vendor authentication
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    inventory = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='product_images/', blank=True)
    # product_type = models.ForeignKey(ProductType, related_name='products', on_delete=models.SET_NULL, null=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)  # Default 10% admin commission
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    key = models.CharField(max_length=255)

    def __str__(self):
        return self.key


class AttributeValue(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.value}: ${self.price}"

class User(AbstractUser):
    # Custom related_name to avoid clashes
    groups = models.ManyToManyField(Group, related_name='catalog_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='catalog_user_permissions')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    vendor_id = models.IntegerField()  # Placeholder for vendor association
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def admin_earnings(self):
        """Calculate admin's share from the order."""
        return (self.total_price * self.product.commission_rate) / 100

    @property
    def vendor_earnings(self):
        """Calculate vendor's share from the order."""
        return self.total_price - self.admin_earnings

    def __str__(self):
        return f"Order {self.id} - {self.product.name} - {self.status}"



# SalesSummary model (optional for faster dashboard calculations)
class SalesSummary(models.Model):
    vendor_id = models.IntegerField()  # Vendor associated with the summary
    total_sales = models.PositiveIntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sales Summary for Vendor {self.vendor_id}"