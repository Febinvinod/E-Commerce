from rest_framework import serializers
from .models import CartItem
<<<<<<< HEAD
from rest_framework import serializers
from .models import Address, ShippingMethod, Order
=======
>>>>>>> 02eee68f634674889b7fefbf145db846b2c87196

class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']
<<<<<<< HEAD


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [field.name for field in Address._meta.fields if field.name != 'session_key']

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'cost']

class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    shipping_method_id = serializers.IntegerField()
=======
>>>>>>> 02eee68f634674889b7fefbf145db846b2c87196
