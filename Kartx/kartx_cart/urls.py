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
from .views import CartView, AddToCartView, UpdateCartItemView, RemoveCartItemView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/remove/<int:product_id>/', RemoveCartItemView.as_view(), name='remove-cart-item'),

    # Address endpoints
    path('address/', AddressView.as_view(), name='address'),  # Add or get addresses

    # Shipping Methods endpoint
    path('shipping-methods/', ShippingMethodsView.as_view(), name='shipping_methods'),  # Get available shipping methods

    # Checkout endpoint
    path('checkout/', CheckoutView.as_view(), name='checkout'),  # Checkout process
]


