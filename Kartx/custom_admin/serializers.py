from rest_framework import serializers
from .models import CustomUser, Vendor, Product, Sale

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Vendor
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = Product
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = Sale
        fields = '__all__'


