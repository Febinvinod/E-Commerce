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
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

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
        """Update the status of an order and notify the user."""
        order_status = get_object_or_404(OrderStatus, order_id=order_id, order__cart__user=request.user)
        serializer = OrderStatusSerializer(order_status, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # Send email notification
            self.send_email_notification(order_status)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_email_notification(self, order_status):
        """Send an email notification to the user when the order status is updated."""
        user_email = order_status.order.cart.user.email
        user_name = order_status.order.cart.user.name
        order_id = order_status.order.id
        status = order_status.status  # Assuming `status` is a field in OrderStatus
        
        # Construct the email subject and body
        subject = f"Order #{order_id} Status Update"
        message = (
            f"Dear {user_name},\n\n"
            f"Your order with ID #{order_id} has been updated.\n"
            f"The new status is: {status}.\n\n"
            f"Thank you for shopping with us!\n\n"
            f"Best regards,\n"
            f"Your E-commerce Team"
        )

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Define this in settings.py
            [user_email],
            fail_silently=False,
        )

    