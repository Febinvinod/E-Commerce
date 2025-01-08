from django.urls import path
from .views import CartView, AddToCartView, UpdateCartItemView, RemoveCartItemView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/remove/<int:product_id>/', RemoveCartItemView.as_view(), name='remove-cart-item'),
]
