from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import RazorpayOrder, PaymentNew, PaymentSuccess
from kartx_cart.models import Cart
#from .serializers import CartSerializer, CartItemSerializer, TransactionHistorySerializer
import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from kartx_cart.models import Cart, Order
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
import razorpay
from datetime import datetime

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
                    "total_price": existing_order.order.total_cost,  # Fetching the total cost from the related order
                    "currency": "INR",
                }, status=status.HTTP_200_OK)

            # Check if an order does not exist for the cart
            order = get_object_or_404(Order, cart=cart)

            # Calculate the total amount for the order (total_cost)
            total = order.total_cost

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

            payment_url = f"https://checkout.razorpay.com/v1/checkout.js?order_id={razorpay_order['id']}"

            return Response({
                "razorpay_order_id": razorpay_order['id'],
                "total_price": total,
                "currency": "INR",
                "payment_url": payment_url,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def payment_page(request):
    razorpay_key = settings.RAZORPAY_KEY_ID  # Fetch the key from settings
    return render(request, "payment_page.html", {"razorpay_key": razorpay_key})
class RazorpayTransactionHistoryAPIView(APIView):
    def get(self, request, order_id=None):
        try:
            # Initialize Razorpay client with credentials
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            
            if not order_id:
                return Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the order details using Razorpay API
            order = razorpay_client.order.fetch(order_id)
            
            # Retrieve the payments associated with the order
            payments = razorpay_client.payment.all({"order_id": order_id})
            
            if not payments['items']:
                return Response({"message": "No payments found for this order."}, status=status.HTTP_404_NOT_FOUND)
            
            # Prepare response with payment details
            payment_data = []
            for payment in payments['items']:
                payment_data.append({
                    "payment_id": payment['id'],
                    "amount": payment['amount'] / 100,  # Convert from paise to INR
                    "currency": payment['currency'],
                    "status": payment['status'],
                    "payment_method": payment['method'],
                    "created_at": payment['created_at'],
                })

            return Response({
                "order_id": order_id,
                "payments": payment_data
            }, status=status.HTTP_200_OK)

        except razorpay.errors.RazorpayError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# class SaveRazorpayPaymentsAPIView(APIView):
#     def get(self, request):
#         try:
#             # Initialize Razorpay client with credentials
#             razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            
#             # Set pagination parameters
#             count = int(request.GET.get('count', 10))  # Number of payments per page
#             skip = int(request.GET.get('skip', 0))  # Pagination offset (skip number of records)
            
#             # Fetch payments from Razorpay
#             payments = razorpay_client.payment.all({"count": count, "skip": skip})

#             # Log the full response from Razorpay for debugging purposes
#             print(payments)  # Check the actual structure of the response

#             # If no payments are found
#             if not payments['items']:
#                 return Response({"message": "No transactions found."}, status=status.HTTP_404_NOT_FOUND)

#             # Iterate through the payments and save them to the database
#             for payment in payments['items']:
#                 if not PaymentNew.objects.filter(payment_id=payment['id']).exists():  # Updated model reference
#                     # Convert created_at (Unix timestamp) to a datetime object
#                     created_at = datetime.fromtimestamp(payment['created_at'])

#                     PaymentNew.objects.create(
#                         payment_id=payment['id'],
#                         amount=payment['amount'] / 100,  # Convert from paise to INR
#                         currency=payment['currency'],
#                         status=payment['status'],
#                         payment_method=payment['method'],
#                         created_at=created_at,  # Store the converted datetime
#                         order_id=payment['order_id'],
#                         customer_id=payment.get('customer_id', None)
#                     )

#             # Check if 'has_more' exists, then return the response
#             has_more = payments.get('has_more', False)  # Default to False if not present
#             return Response({
#                 "message": "Payments saved successfully.",
#                 "total_payments_saved": len(payments['items']),
#                 "has_more": has_more,  # Safely access 'has_more'
#             }, status=status.HTTP_200_OK)

#         except Exception as e:  # Catching all exceptions to diagnose better
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class SaveRazorpayPaymentsAPIView(APIView):
    def get(self, request):
        try:
            # Initialize Razorpay client with credentials
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            
            # Set pagination parameters
            count = int(request.GET.get('count', 10))  # Number of payments per page
            skip = int(request.GET.get('skip', 0))  # Pagination offset (skip number of records)
            
            # Fetch payments from Razorpay
            payments = razorpay_client.payment.all({"count": count, "skip": skip})

            # Log the full response from Razorpay for debugging purposes
            print(payments)  # Check the actual structure of the response

            # If no payments are found
            if not payments['items']:
                return Response({"message": "No transactions found."}, status=status.HTTP_404_NOT_FOUND)

            # Iterate through the payments and save them to the database
            for payment in payments['items']:
                if not PaymentNew.objects.filter(payment_id=payment['id']).exists():  # Updated model reference
                    # Convert created_at (Unix timestamp) to a datetime object
                    created_at = datetime.fromtimestamp(payment['created_at'])

                    # Save the payment details into PaymentNew model
                    PaymentNew.objects.create(
                        payment_id=payment['id'],
                        amount=payment['amount'] / 100,  # Convert from paise to INR
                        currency=payment['currency'],
                        status=payment['status'],
                        payment_method=payment['method'],
                        created_at=created_at,  # Store the converted datetime
                        order_id=payment['order_id'],
                        customer_id=payment.get('customer_id', None)
                    )

            # Now let's check the RazorpayOrder model and update PaymentSuccess if order_id matches
            razorpay_orders = RazorpayOrder.objects.all()
            payment_news = PaymentNew.objects.all()

            # Iterate through each RazorpayOrder and check if order_id exists in PaymentNew
            for razorpay_order in razorpay_orders:
                payment_new = payment_news.filter(order_id=razorpay_order.order_id).first()

                if payment_new and payment_new.status.lower() == 'captured':
                    # If payment status is 'paid' and matching order_id exists, create PaymentSuccess
                    if not PaymentSuccess.objects.filter(order_id=razorpay_order.order_id).exists():
                        # Create PaymentSuccess entry
                        paymentsuccess=PaymentSuccess.objects.create(
                            cart_id=razorpay_order.cart,  # Reference the cart associated with the order
                            order_id=razorpay_order.order_id,
                            payment_status='paid'
                        )
                        # Update RazorpayOrder payment status to 'paid'
                        #razorpay_order.payment_status = RazorpayOrder.PaymentStatus.PAID
                        paymentsuccess.save()

            # Check if 'has_more' exists, then return the response
            has_more = payments.get('has_more', False)  # Default to False if not present
            return Response({
                "message": "Payments saved successfully and PaymentSuccess updated.",
                "total_payments_saved": len(payments['items']),
                "has_more": has_more,  # Safely access 'has_more'
            }, status=status.HTTP_200_OK)

        except Exception as e:  # Catching all exceptions to diagnose better
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)