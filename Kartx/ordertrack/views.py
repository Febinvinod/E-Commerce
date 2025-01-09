from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OrderStatus
from kartx_cart.models import Order
from .serializers import OrderSerializer, OrderStatusSerializer
from django.shortcuts import get_object_or_404

class OrderListView(APIView):
    def get(self, request):
        """Get the list of all orders for the user."""
        if request.user.is_authenticated:
            orders = Order.objects.filter(cart__user=request.user)
        else:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderStatusView(APIView):
    def get(self, request, order_id):
        """Get the status of a specific order."""
        order_status = get_object_or_404(OrderStatus, order_id=order_id)
        serializer = OrderStatusSerializer(order_status)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, order_id):
        """Update the status of an order."""
        order_status = get_object_or_404(OrderStatus, order_id=order_id)
        serializer = OrderStatusSerializer(order_status, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
