from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import AddCartItemSerializer, CartItemSerializer
from .models import Cart, Address, ShippingMethod, Order
from .serializers import AddressSerializer, ShippingMethodSerializer, CheckoutSerializer
from django.shortcuts import get_object_or_404

class AddressView(APIView):
    def get(self, request):
        """Get all addresses for the user."""
        if request.user.is_authenticated:
            addresses = Address.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key
            addresses = Address.objects.filter(session_key=session_key)

        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add a new address."""
        if not request.user.is_authenticated and not request.session.session_key:
            request.session.create()

        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user if request.user.is_authenticated else None, 
                            session_key=request.session.session_key)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShippingMethodsView(APIView):
    def get(self, request):
        """Get all available shipping methods."""
        shipping_methods = ShippingMethod.objects.all()
        serializer = ShippingMethodSerializer(shipping_methods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        """Add a new shipping method."""
        serializer = ShippingMethodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckoutView(APIView):
    def post(self, request):
        """Process checkout."""
        cart = get_object_or_404(Cart, user=request.user if request.user.is_authenticated else None,
                                 session_key=request.session.session_key if not request.user.is_authenticated else None)

        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            address_id = serializer.validated_data['address_id']
            shipping_method_id = serializer.validated_data['shipping_method_id']

            address = get_object_or_404(Address, id=address_id)
            shipping_method = get_object_or_404(ShippingMethod, id=shipping_method_id)

            # Calculate total cost
            total_cost = sum(item.quantity * 10 for item in cart.items.all())  # Example: Replace '10' with actual product cost
            total_cost += shipping_method.cost

            # Create Order
            order = Order.objects.create(
                cart=cart, 
                address=address, 
                shipping_method=shipping_method,
                total_cost=total_cost
            )

            return Response({"message": "Checkout successful.", "order_id": order.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Simulated ProductService for product validation
class ProductService:
    @staticmethod
    def get_product(product_id):
        # Replace this with actual product validation
        # For now, assume any product_id <= 100 exists
        return product_id <= 100

class CartView(APIView):
    def get(self, request):
        """List all items in the user's cart."""

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        cart_items = cart.items.all()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToCartView(APIView):
    def post(self, request):
        """Add a product to the cart."""
        # Determine if the user is anonymous or authenticated
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            # Use session key for anonymous users
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        # Process the cart item
        serializer = AddCartItemSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data["product_id"]
            quantity = serializer.validated_data["quantity"]

            # Add or update the product in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
            if not created:
                cart_item.quantity += quantity
            cart_item.save()

            return Response({"message": "Product added to cart."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateCartItemView(APIView):
    def put(self, request, product_id):
        """Update the quantity of a product in the cart."""

        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
        else:
            if not request.session.session_key:
                return Response({"error": "Session not initialized."}, status=status.HTTP_400_BAD_REQUEST)
            session_key = request.session.session_key
            cart = get_object_or_404(Cart, session_key=session_key)

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        quantity = request.data.get("quantity")
        if not quantity or int(quantity) < 1:
            return Response({"error": "Quantity must be at least 1."}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = quantity
        cart_item.save()
        return Response({"message": "Cart updated successfully."}, status=status.HTTP_200_OK)

class RemoveCartItemView(APIView):
    def delete(self, request, product_id):
        """Remove a product from the cart."""

        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
        else:
            if not request.session.session_key:
                return Response({"error": "Session not initialized."}, status=status.HTTP_400_BAD_REQUEST)
            session_key = request.session.session_key
            cart = get_object_or_404(Cart, session_key=session_key)

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()

        return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
