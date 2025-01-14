from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OrderStatus
from kartx_cart.models import Order
from .serializers import OrderSerializer, OrderStatusSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class OrderListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get the list of all orders for the user."""
        # Get all OrderStatus entries related to the user
        orders_status = OrderStatus.objects.filter(order__cart__user=request.user)

        # Prepare a list to hold combined data
        combined_data = []

        # Loop through each OrderStatus and manually serialize the associated Order
        for order_status in orders_status:
            # Serialize the associated Order model with product details via CartItems
            order_data = OrderSerializer(order_status.order).data
            
            # Prepare the final combined data with both Order and OrderStatus
            combined_entry = {
                'order': order_data,
                'status': order_status.status,
                'updated_at': order_status.updated_at
            }
            combined_data.append(combined_entry)

        return Response(combined_data, status=status.HTTP_200_OK)

class OrderStatusView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        """Get the status of a specific order."""
        order = get_object_or_404(Order, id=order_id, cart__user=request.user)
        order_status = get_object_or_404(OrderStatus, order_id=order_id)
        serializer = OrderStatusSerializer(order_status)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, order_id):
        """Update the status of an order."""
        order_status = get_object_or_404(OrderStatus, order_id=order_id, order__cart__user=request.user)
        serializer = OrderStatusSerializer(order_status, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
