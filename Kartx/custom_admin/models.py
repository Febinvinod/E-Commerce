from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    # Set custom related names for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='custom_admin_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_admin_user_permissions', blank=True)

    def __str__(self):
        return self.username


class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor_profile')
    approved = models.BooleanField(default=False)  # Admin will approve vendor

    def __str__(self):
        return self.user.username

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class Sale(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='sales')
    revenue = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Sale by {self.vendor.user.username} - {self.revenue}"

