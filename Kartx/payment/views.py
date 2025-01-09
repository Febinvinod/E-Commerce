from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404


class AddItemToCartAPIView(APIView):
    def post(self, request, cart_id):
        """
        Add items to the cart. Expects 'product_name', 'quantity', and 'price_per_unit'.
        """
        try:
            # Get the cart by ID
            cart = get_object_or_404(Cart, id=cart_id)

            # Get item data from request
            product_name = request.data.get('product_name')
            quantity = request.data.get('quantity', 1)
            price_per_unit = request.data.get('price_per_unit')

            # Validate input
            if not product_name or not price_per_unit:
                return Response({"error": "Product name and price are required."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the CartItem
            cart_item = CartItem.objects.create(
                cart=cart,
                product_name=product_name,
                quantity=quantity,
                price_per_unit=price_per_unit
            )

            # Recalculate the cart total
            total = cart.calculate_total()

            # Return updated cart info
            cart_serializer = CartSerializer(cart)
            return Response({
                "cart": cart_serializer.data,
                "total_price": total
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateRazorpayOrderAPIView(APIView):
    def post(self, request, cart_id):
        """
        Create a Razorpay order based on the total amount of the cart.
        """
        try:
            # Get the cart by ID
            cart = get_object_or_404(Cart, id=cart_id)

            # Calculate the total amount for the cart
            total = cart.calculate_total()
            print(f"Cart Total: {total}")

            # Check if total is valid
            if total <= 0:
                return Response({"error": "Cart total must be greater than 0."}, status=status.HTTP_400_BAD_REQUEST)

            # Initialize Razorpay client with credentials from settings
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            print("Razorpay Client Initialized")

            # Create Razorpay order
            razorpay_order = razorpay_client.order.create({
                "amount": int(total * 100),  # Razorpay expects amount in paise (100 paise = 1 INR)
                "currency": "INR",
                "payment_capture": "1"
            })
            print(f"Razorpay Order Created: {razorpay_order}")

            # Return the Razorpay order ID and the total price for frontend use
            return Response({
                "razorpay_order_id": razorpay_order['id'],
                "total_price": total,
                "currency": "INR",
            }, status=status.HTTP_200_OK)

        except razorpay.errors.BadRequestError as e:
            print(f"Bad Request Error: {str(e)}")
            return Response({"error": f"Razorpay Bad Request Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except razorpay.errors.ServerError as e:
            print(f"Server Error: {str(e)}")
            return Response({"error": f"Razorpay Server Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except razorpay.errors.ConnectionError as e:
            print(f"Connection Error: {str(e)}")
            return Response({"error": f"Razorpay Connection Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateCartAPIView(APIView):
    def post(self, request):
        """
        Create a new cart. No user authentication is required for testing purposes.
        """
        try:
            # Create the cart without a user
            cart = Cart.objects.create(user=None)  # Set user to None for testing

            return Response({"cart_id": cart.id}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPaymentAPIView(APIView):
    def post(self, request):
        """
        Verify Razorpay payment by validating the payment signature.
        """
        try:
            data = request.data

            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")

            if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                return Response({"error": "Missing required parameters."}, status=status.HTTP_400_BAD_REQUEST)

            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

            # Prepare data for signature verification
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            }

            # Verify the payment signature using Razorpay's utility method
            razorpay_client.utility.verify_payment_signature(params_dict)

            # If signature is valid, you can update payment status or proceed
            # For example, you can update the order or cart status here

            return Response({"message": "Payment verified successfully."}, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError as e:
            # If signature verification fails
            return Response({"error": f"Signature verification failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle any other unexpected errors
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
