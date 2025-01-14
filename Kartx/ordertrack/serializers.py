from rest_framework import serializers
from .models import OrderStatus
from kartx_cart.models import Order, CartItem,ShippingMethod
from catalog.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'brand', 'image', 'rating']  # Customize based on your fields

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cart.items', many=True)  # Add cart items with product details
    shipping_method_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'address', 'shipping_method_name', 'total_cost', 'created_at', 'items']  # Add items field to include product details
    
    def get_shipping_method_name(self, obj):
        # Fetch the name of the related ShippingMethod object
        return obj.shipping_method.name if obj.shipping_method else None

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ['order', 'status', 'updated_at']
