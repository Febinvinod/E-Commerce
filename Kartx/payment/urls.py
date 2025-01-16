from django.urls import path
from . import views  # Define an app name for namespaced reverse()
urlpatterns = [
    path('create-razorpay-order/<int:cart_id>/', views.CreateRazorpayOrderAPIView.as_view(), name='create_razorpay_order'),
    path('api/razorpay-transaction-history/<str:order_id>/', views.RazorpayTransactionHistoryAPIView.as_view(), name='razorpay-transaction-history'),
    path('api/save-razorpay-payments/', views.SaveRazorpayPaymentsAPIView.as_view(), name='save-razorpay-payments'),
    path('pay/', views.payment_page, name='redirect_to_payment'),
]