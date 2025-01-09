from django.urls import path
from . import views

urlpatterns = [
    # URL for creating a cart
    path('cart/create/', views.CreateCartAPIView.as_view(), name='create_cart'),

    # URL for adding item to the cart
    path('cart/<int:cart_id>/add-item/', views.AddItemToCartAPIView.as_view(), name='add_item_to_cart'),

    # URL for creating Razorpay order
    path('cart/<int:cart_id>/create-order/', views.CreateRazorpayOrderAPIView.as_view(), name='create_razorpay_order'),

    # URL for verifying Razorpay payment
    path('payment/verify/', views.VerifyPaymentAPIView.as_view(), name='verify_payment'),
    path('checkout/<int:cart_id>/', views.checkout_view, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('payment-details/<int:cart_id>/', views.RetrievePaymentDetailsAPIView.as_view(), name='payment_details'),
    path('transaction-history/', views.TransactionHistoryAPIView.as_view(), name='transaction-history'),
]
