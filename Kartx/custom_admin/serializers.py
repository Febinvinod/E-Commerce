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
    vendor_name = serializers.CharField(source='vendor.user.username', read_only=True)
    vendor_id = serializers.IntegerField(source='vendor.id', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'vendor_name', 'vendor_id']

class SaleSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = Sale
        fields = '__all__'


