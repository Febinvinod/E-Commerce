from rest_framework import serializers
from .models import *
from accounts.models import *
from catalog.serializers import *


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
    vendor_name = serializers.SerializerMethodField()
    vendor_id = serializers.IntegerField(source='vendor.id', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['vendor']

    def get_vendor_name(self, obj):
        return obj.vendor.company_name if obj.vendor else None

    def create(self, validated_data):
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Request context is missing.")

        user = request.user
        vendor = getattr(user, 'vendor_profile', None)  # Use the correct related name

        if not vendor:
            raise serializers.ValidationError("The authenticated user does not have a vendor profile.")

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

class ProductDetailSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    vendor_id = serializers.IntegerField(source='vendor.id', read_only=True)
    category_name = serializers.SerializerMethodField()
    attributes = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'inventory', 'brand', 'rating', 'image', 
                  'commission_rate', 'vendor', 'category', 'vendor_id', 
                  'vendor_name', 'category_name', 'attributes']
        read_only_fields = ['vendor']

    def get_vendor_name(self, obj):
        return obj.vendor.company_name if obj.vendor else None

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
class ProductUserListing(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    vendor_id = serializers.IntegerField(source='vendor.id', read_only=True)
    category_name = serializers.SerializerMethodField()
    attributes = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'inventory', 'brand', 'rating', 'image', 
                   'vendor', 'category', 'vendor_id', 
                  'vendor_name', 'category_name', 'attributes']
        read_only_fields = ['vendor']

    def get_vendor_name(self, obj):
        return obj.vendor.company_name if obj.vendor else None

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    