from django.urls import path
<<<<<<< HEAD
from .views import (
    CartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView,
    AddressView,
    ShippingMethodsView,
    CheckoutView,
)
=======
from .views import CartView, AddToCartView, UpdateCartItemView, RemoveCartItemView

>>>>>>> 02eee68f634674889b7fefbf145db846b2c87196
urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/remove/<int:product_id>/', RemoveCartItemView.as_view(), name='remove-cart-item'),
<<<<<<< HEAD
    # Address endpoints
    path('address/', AddressView.as_view(), name='address'),  # Add or get addresses

    # Shipping Methods endpoint
    path('shipping-methods/', ShippingMethodsView.as_view(), name='shipping_methods'),  # Get available shipping methods

    # Checkout endpoint
    path('checkout/', CheckoutView.as_view(), name='checkout'),  # Checkout process
]

=======
]
>>>>>>> 02eee68f634674889b7fefbf145db846b2c87196
