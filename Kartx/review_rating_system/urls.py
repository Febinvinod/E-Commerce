from django.urls import path
from .views import ProductListView, ReviewRatingCreateView, ReviewRatingListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('reviews/add/', ReviewRatingCreateView.as_view(), name='add-review'),
    path('reviews/<int:product_id>/', ReviewRatingListView.as_view(), name='product-reviews'),
]
