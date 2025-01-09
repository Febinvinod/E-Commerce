from rest_framework import serializers
from .models import OrderStatus
from kartx_cart.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'address', 'shipping_method', 'total_cost', 'created_at']

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ['order', 'status', 'updated_at']
