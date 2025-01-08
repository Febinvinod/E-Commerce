# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('send_notifications/<str:payment_id>/', views.send_notifications, name='send_notifications'),
]
