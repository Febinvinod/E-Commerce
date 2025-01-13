from rest_framework import serializers
from .models import *
from accounts.models import Vendor


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'attribute', 'value', 'price']


class ProductAttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ['id', 'product', 'key', 'values']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['vendor']  # Mark vendor as read-only
        
    def create(self, validated_data):
        # Automatically associate the authenticated vendor
        request = self.context.get('request')  # Safely access 'request' from context
        if not request:
            raise serializers.ValidationError("Request context is missing.")

        user = request.user

        # Safely access the vendor profile
        vendor = getattr(user, 'vendor_profile', None)  # Using the correct related_name
        if not vendor:
            raise serializers.ValidationError("The authenticated user does not have a vendor profile.")

        # Create the product with the associated vendor
        product = Product.objects.create(vendor=vendor, **validated_data)
        return product



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role', 'phone']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_picture', 'phone_number']
        read_only_fields = ['user']

