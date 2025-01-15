from django.urls import path
from . import views
app_name = 'payment'  # Define an app name for namespaced reverse()
urlpatterns = [
    path('create-razorpay-order/<int:cart_id>/', views.CreateRazorpayOrderAPIView.as_view(), name='create_razorpay_order'),
]