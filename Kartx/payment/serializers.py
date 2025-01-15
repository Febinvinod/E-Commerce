# serializers.py
from rest_framework import serializers
from kartx_cart.models import Cart, CartItem
from .models import RazorpayOrder

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product_name', 'quantity', 'price_per_unit']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items']
class TransactionHistorySerializer(serializers.ModelSerializer):
    # If RazorpayOrder is a related model, you can serialize it like this
    order_id = serializers.CharField(source='razorpayorder.order_id')
    payment_id = serializers.CharField(source='razorpayorder.payment_id')
    payment_status = serializers.CharField(source='razorpayorder.payment_status')

    class Meta:
        model = Cart
        fields = ['id', 'order_id', 'payment_id', 'payment_status']
