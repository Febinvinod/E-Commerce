from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import AddCartItemSerializer, CartItemSerializer
from .models import Cart, Address, ShippingMethod, Order
from .serializers import AddressSerializer, ShippingMethodSerializer, CheckoutSerializer
from django.shortcuts import get_object_or_404
from ordertrack.models import OrderStatus
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



class AddressView(APIView):
    def get(self, request):
        """Get all addresses."""
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add a new address."""
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        """Process checkout."""
        # Get the cart ID from the session
        cart_id = request.data.get('cart_id')
        if not cart_id:
            return Response({"error": "Cart ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the cart for the logged-in user
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)

        # Validate checkout data
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            address_id = serializer.validated_data['address_id']
            shipping_method_id = serializer.validated_data['shipping_method_id']

            # Get address and shipping method
            address = get_object_or_404(Address, id=address_id)
            shipping_method = get_object_or_404(ShippingMethod, id=shipping_method_id)

            # Calculate total cost
            total_cost = sum(
                item.quantity * 10 for item in cart.items.all()
            )  # Example: Replace '10' with actual product cost
            total_cost += shipping_method.cost

            # Create Order
            order = Order.objects.create(
                cart=cart,
                address=address,
                shipping_method=shipping_method,
                total_cost=total_cost
            )
            # Create corresponding OrderStatus
            OrderStatus.objects.create(order=order)

            cart.items.filter(visible=True).update(visible=False)

            # Create a new cart for the user
            new_cart = Cart.objects.create(user=request.user)
            request.session['cart_id'] = new_cart.id

            return Response({
                "message": "Checkout successful.",
                "order_id": order.id,
                "new_cart_id": new_cart.id  # Return the new cart ID if needed
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Simulated ProductService for product validation
class ProductService:
    @staticmethod
    def get_product(product_id):
        # Replace this with actual product validation
        # For now, assume any product_id <= 100 exists
        return product_id <= 100



class CartView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        """List all items in the cart and return the cart ID."""
        cart_id = request.session.get('cart_id', None)

        if not cart_id:
            return Response({"error": "No cart found."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the cart for the current user
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)

        # Serialize the cart items
        cart_items = cart.items.filter(visible=True)  
        serializer = CartItemSerializer(cart_items, many=True)

        # Return the cart ID along with cart items
        return Response(
            {
                "cart_id": cart.id,  # Include cart ID
                "items": serializer.data
            },
            status=status.HTTP_200_OK
        )



class AddToCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        """Add a product to the cart."""
        
        # Retrieve the cart for the logged-in user
        cart_id = request.session.get('cart_id', None)

        if not cart_id:
            # Create a new cart for the user if not existing
            cart = Cart.objects.create(user=request.user)  # Associate the cart with the user
            request.session['cart_id'] = cart.id  # Store the cart ID in the session
        else:
            try:
                cart = Cart.objects.get(id=cart_id, user=request.user)  # Retrieve cart for the logged-in user
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=request.user)  # Create a new cart and associate it with the user
                request.session['cart_id'] = cart.id

        # Process the cart item
        serializer = AddCartItemSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data["product_id"]
            quantity = serializer.validated_data["quantity"]

            # Add or update the product in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
            if not created:
                cart_item.quantity += quantity  # Update quantity if the product already exists
            else:
                cart_item.quantity = quantity  # Set the quantity when a new item is created
            cart_item.save()

            return Response({
                "message": "Product added to cart.",
                "cart_id": cart.id  # Return the cart ID to the frontend (optional)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCartItemView(APIView):
    def put(self, request, product_id):
        """Update the quantity of a product in the cart."""
        # Retrieve the cart ID from the session
        cart_id = request.session.get('cart_id', None)

        if not cart_id:
            return Response({"error": "No cart found."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the cart using the cart_id
        cart = get_object_or_404(Cart, id=cart_id)

        # Fetch the cart item associated with the cart and product_id
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        # Get the new quantity from the request data
        quantity = request.data.get("quantity")
        if not quantity or int(quantity) < 1:
            return Response({"error": "Quantity must be at least 1."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the cart item quantity
        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Cart updated successfully."}, status=status.HTTP_200_OK)


class RemoveCartItemView(APIView):
    def delete(self, request, product_id):
        """Remove a product from the cart."""
        # Retrieve the cart ID from the session
        cart_id = request.session.get('cart_id', None)

        if not cart_id:
            return Response({"error": "No cart found."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the cart using the cart_id
        cart = get_object_or_404(Cart, id=cart_id)

        # Fetch the cart item associated with the cart and product_id
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        # Delete the cart item
        cart_item.delete()

        return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
