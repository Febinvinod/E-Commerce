from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, RazorpayOrder
from .serializers import CartSerializer, CartItemSerializer, TransactionHistorySerializer
import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404



class CreateRazorpayOrderAPIView(APIView):
    def post(self, request, cart_id):
        try:
            # Get the cart by ID
            cart = get_object_or_404(Cart, id=cart_id)

            # Check if an order already exists for this cart
            existing_order = RazorpayOrder.objects.filter(cart=cart).first()

            if existing_order:
                # If order exists, reuse the existing order ID
                return Response({
                    "razorpay_order_id": existing_order.order_id,
                    "total_price": cart.calculate_total(),
                    "currency": "INR",
                }, status=status.HTTP_200_OK)

            # Calculate the total amount for the cart
            total = cart.calculate_total()

            # Check if total is valid
            if total <= 0:
                return Response({"error": "Cart total must be greater than 0."}, status=status.HTTP_400_BAD_REQUEST)

            # Initialize Razorpay client with credentials from settings
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

            # Create Razorpay order
            razorpay_order = razorpay_client.order.create({
                "amount": int(total * 100),  # Razorpay expects amount in paise (100 paise = 1 INR)
                "currency": "INR",
                "payment_capture": "1"
            })

            # Save the Razorpay order with the cart association
            RazorpayOrder.objects.create(cart=cart, order_id=razorpay_order['id'])

            return Response({
                "razorpay_order_id": razorpay_order['id'],
                "total_price": total,
                "currency": "INR",
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
def checkout_view(request, cart_id):
    """
    View to render the Razorpay checkout page.
    """
    # Get the cart details by cart_id
    cart = get_object_or_404(Cart, id=cart_id)
    
    # You can pass additional cart details if needed (e.g., cart items, total, etc.)
    return render(request, 'checkout.html', {'cart_id': cart.id, 'total_price': cart.calculate_total(),'razorpay_key': settings.RAZORPAY_KEY_ID})
def order_confirmation(request):
    return render(request, 'order_confirmation.html')

class RetrievePaymentDetailsAPIView(APIView):
    def get(self, request, cart_id):
        try:
            cart = get_object_or_404(Cart, id=cart_id)

            # Get the Razorpay order for the cart
            razorpay_order = RazorpayOrder.objects.get(cart=cart)

            return Response({
                "razorpay_order_id": razorpay_order.order_id,
                "razorpay_payment_id": razorpay_order.payment_id,
                "payment_status": razorpay_order.payment_status,
                "total_price": cart.calculate_total(),
                "currency": "INR"
            }, status=status.HTTP_200_OK)

        except RazorpayOrder.DoesNotExist:
            return Response({"error": "No Razorpay order found for this cart."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class TransactionHistoryAPIView(APIView):
    def get(self, request):
        """
        Get the transaction history (cart ID, order ID, payment ID, payment status).
        """
        try:
            # Get all carts with associated payment details (order_id, payment_id, status)
            carts = Cart.objects.filter(razorpayorder__isnull=False)  # Make sure you have related payment info

            # Serialize the carts with transaction data
            serializer = TransactionHistorySerializer(carts, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
