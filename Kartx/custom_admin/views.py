# from django.shortcuts import get_object_or_404
# from rest_framework import viewsets
# from rest_framework.permissions import AllowAny
# from .models import CustomUser, Vendor, Product, Sale
# from .serializers import CustomUserSerializer, VendorSerializer, ProductSerializer, SaleSerializer

# class CustomUserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = [AllowAny]

# class VendorViewSet(viewsets.ModelViewSet):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         vendor = serializer.save()
#         vendor.user.is_vendor = True
#         vendor.user.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [AllowAny]

#     def perform_create(self, serializer):
#         serializer.save(vendor=get_object_or_404(Vendor, user=self.request.user))

# class SaleViewSet(viewsets.ModelViewSet):
#     queryset = Sale.objects.all()
#     serializer_class = SaleSerializer
#     permission_classes = [AllowAny]

from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import CustomUser, Vendor, Product, Sale
from .serializers import CustomUserSerializer, VendorSerializer, ProductSerializer, SaleSerializer
from accounts.models import*

# CustomUser API View
# class CustomUserAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         # Filter users based on authentication or session data
#         logged_in_users = CustomUser.objects.filter(is_authenticated=True)
#         serializer = CustomUserSerializer(logged_in_users, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomUserAPIView(APIView):

    def get(self, request):
        # Fetch all registered users
        queryset = User.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
# Vendor API View
class VendorAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Vendor.objects.all()
        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = serializer.save()
        vendor.user.is_vendor = True
        vendor.user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Product API View
class ProductAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(vendor=get_object_or_404(Vendor, user=self.request.user))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Sale API View
class SaleAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Sale.objects.all()
        serializer = SaleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

