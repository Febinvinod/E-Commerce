from django.db import models

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
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
    product_type = models.ForeignKey(ProductType, related_name='products', on_delete=models.SET_NULL, null=True)

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



