from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView,
    AddressView,
    ShippingMethodsView,
    CheckoutView,
)
<<<<<<< HEAD
=======
from .views import CartView, AddToCartView, UpdateCartItemView, RemoveCartItemView

>>>>>>> f637e21a8585921906c33f792ed42b1d3582d59e
urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/remove/<int:product_id>/', RemoveCartItemView.as_view(), name='remove-cart-item'),
<<<<<<< HEAD
=======

>>>>>>> f637e21a8585921906c33f792ed42b1d3582d59e
    # Address endpoints
    path('address/', AddressView.as_view(), name='address'),  # Add or get addresses

    # Shipping Methods endpoint
    path('shipping-methods/', ShippingMethodsView.as_view(), name='shipping_methods'),  # Get available shipping methods

    # Checkout endpoint
    path('checkout/', CheckoutView.as_view(), name='checkout'),  # Checkout process
]

<<<<<<< HEAD
=======

>>>>>>> f637e21a8585921906c33f792ed42b1d3582d59e
