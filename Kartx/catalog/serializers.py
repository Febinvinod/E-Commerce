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
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_picture', 'phone_number']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = validated_data.pop('user')
        return UserProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance