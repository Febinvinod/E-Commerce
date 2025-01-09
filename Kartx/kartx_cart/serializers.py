from rest_framework import serializers
from .models import CartItem
from rest_framework import serializers
from .models import Address, ShippingMethod, Order

class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'cost']

class CheckoutSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()  # Add cart_id to the serializer
    address_id = serializers.IntegerField()
    shipping_method_id = serializers.IntegerField()

