from django.urls import path
from .views import OrderListView, OrderStatusView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:order_id>/status/', OrderStatusView.as_view(), name='order-status'),
]
