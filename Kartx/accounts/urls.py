# from django.urls import path
# from .views import UserRegistrationView, VendorRegistrationView, LoginView

# urlpatterns = [
#     path('register/user/', UserRegistrationView.as_view(), name='user-register'),
#     path('register/vendor/', VendorRegistrationView.as_view(), name='vendor-register'),
#     path('login/', LoginView.as_view(), name='login'),
# ]

from django.urls import path
from .views import UserRegistrationView, VendorRegistrationView, LoginView

urlpatterns = [
    path('register/user/', UserRegistrationView.as_view(), name='user-register'),
    path('register/vendor/', VendorRegistrationView.as_view(), name='vendor-register'),
    path('login/', LoginView.as_view(), name='login'),
]
