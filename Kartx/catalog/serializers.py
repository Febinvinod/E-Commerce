from rest_framework import serializers
from .models import *


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
    attributes = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'vendor_id', 'name', 'description',
            'inventory', 'category', 'brand', 'rating', 'image','product_type', 'attributes'
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description']
        
        
