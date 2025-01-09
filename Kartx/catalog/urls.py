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
    path('categories/', CategoryAPIView.as_view(), name='category-list'),
    path('products/', ProductAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductAPIView.as_view(), name='product-detail'),
    path('product-types/', ProductTypeListAPIView.as_view(), name='product-type-list'),
    path('products/search/', ProductSearchAPIView.as_view(), name='product-search'),
    path('attributes/', ProductAttributeAPIView.as_view(), name='attribute-list'),
    path('attributes/<int:pk>/', ProductAttributeAPIView.as_view(), name='attribute-detail'),
    path('attributes/product/<int:product_id>/', ProductAttributeAPIView.as_view(), name='product-attributes'),
    path('attribute-values/', AttributeValueAPIView.as_view(), name='attribute-value-list'),
    path('attribute-values/<int:pk>/', AttributeValueAPIView.as_view(), name='attribute-value-detail'),
    path('attribute-values/attribute/<int:attribute_id>/', AttributeValueAPIView.as_view(), name='attribute-value-by-attribute'),
    path('categories/all/', AllCategoriesAPIView.as_view(), name='all-categories'),
    path('products/list/', ProductListAPIView.as_view(), name='product-listing'),
    path('products/search/json/', JSONSearchAPIView.as_view(), name='json-search'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('profile/edit/', UserProfileAPIView.as_view(), name='edit-user-profile'),
    path('vendor/dashboard/', VendorDashboardView.as_view(), name='vendor-dashboard'),
    
]
