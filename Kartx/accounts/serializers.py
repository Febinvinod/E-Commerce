# from rest_framework import serializers
# from .models import User, Vendor

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'name', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)


# class VendorSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Vendor
#         fields = ['id', 'user', 'company_name']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(**user_data, is_vendor=True)
#         return Vendor.objects.create(user=user, **validated_data)

from rest_framework import serializers
from .models import User, Vendor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = ['id', 'user', 'company_name']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, is_vendor=True)
        return Vendor.objects.create(user=user, **validated_data)
