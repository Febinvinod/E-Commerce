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
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import CustomUserViewSet, VendorViewSet, ProductViewSet, SaleViewSet

# router = DefaultRouter()
# router.register(r'users', CustomUserViewSet)
# router.register(r'vendors', VendorViewSet)
# router.register(r'products', ProductViewSet)
# router.register(r'sales', SaleViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
from django.urls import path
from .views import CustomUserAPIView, VendorAPIView, ProductAPIView, SaleAPIView

urlpatterns = [
    path('users/', CustomUserAPIView.as_view(), name='customuser-api'),
    path('vendors/', VendorAPIView.as_view(), name='vendor-api'),
    path('products/', ProductAPIView.as_view(), name='product-api'),
    path('sales/', SaleAPIView.as_view(), name='sale-api'),
]

