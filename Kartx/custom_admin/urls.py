"""
URL configuration for EcommerceApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('users/admin', CustomUserAPIView.as_view(), name='customuser-api'),
    path('users/<int:pk>/', CustomUserAPIView.as_view(), name='user-detail-update'),
    path('vendors/admin', VendorAPIView.as_view(), name='vendor-api'),
    path('vendors/<int:pk>/', VendorAPIView.as_view(), name='vendor-detail-update'),
    path('products/admin', ProductAPIView.as_view(), name='product-api'),
    path('products/admin/<int:pk>/', ProductAPIView.as_view(), name='product-detail'),
    path('sales/admin', SaleAPIView.as_view(), name='sale-api'),
    path('admin/users/<int:pk>/', UserDeleteAPIView.as_view(), name='delete-user'),
    path('admin/vendor/<int:pk>/', VendorDeleteAPIView.as_view(), name='delete-vendor'),
    path('approve/vendor/<int:pk>/', ApproveVendorView.as_view(), name='approve-vendor'),
    path('admin/pending-vendors/', PendingVendorsAPIView.as_view(), name='pending-vendors-list'),
]

