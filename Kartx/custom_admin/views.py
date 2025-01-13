# from django.shortcuts import get_object_or_404
# from rest_framework import status, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from .models import CustomUser, Vendor, Product, Sale
# from .serializers import *
# from accounts.models import*
# from catalog.serializers import *


# class CustomUserAPIView(APIView):

#     def get(self, request):
#         # Fetch all registered users
#         queryset = User.objects.all()
#         serializer = CustomUserSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
# # Vendor API View
# class VendorAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         queryset = Vendor.objects.all()
#         serializer = VendorSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = VendorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         vendor = serializer.save()
#         vendor.user.is_vendor = True
#         vendor.user.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# # Product API View
# class ProductAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         queryset = Product.objects.all()
#         serializer = ProductDetailSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductDetailSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(vendor=get_object_or_404(Vendor, user=self.request.user))
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# # Sale API View
# class SaleAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         queryset = Sale.objects.all()
#         serializer = SaleSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = SaleSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from accounts.models import*
from catalog.serializers import *
from accounts.models import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator

# Custom permission for admin-only access
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

# CustomUser API View
class CustomUserAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = CustomUser.objects.all()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Vendor API View
class VendorAPIView(APIView):
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductDetailSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def delete(self, request, pk=None):
        """
        Delete a product by its ID.
        """
        if not pk:
            return Response(
                {"error": "Product ID (pk) is required for deletion."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch the product or return a 404 if not found
        product = get_object_or_404(Product, pk=pk)

        # Delete the product
        product.delete()

        return Response(
            {"message": f"Product with ID {pk} has been deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )

# Sale API View
class SaleAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Sale.objects.all()
        serializer = SaleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UserDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk=None):
        """
        Delete a user by their ID.
        """
        if not pk:
            return Response(
                {"error": "User ID (pk) is required for deletion."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch the user or return a 404 if not found
        user = get_object_or_404(User, pk=pk)

        # Delete the user
        user.delete()

        return Response(
            {"message": f"User with ID {pk} has been deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )



class VendorDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk=None):
        """
        Delete a vendor by their ID.
        """
        if not pk:
            return Response(
                {"error": "Vendor ID (pk) is required for deletion."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch the vendor or return a 404 if not found
        vendor = get_object_or_404(User ,pk=pk,is_vendor=True)

        # Delete the vendor
        vendor.delete()

        return Response(
            {"message": f"Vendor with ID {pk} has been deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )

class UserListAPIView(APIView):
    """
    View to list all users (admin-only access), directly fetching model fields.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Fetch all users
        users = User.objects.all().values(
            'id', 'email', 'name', 'is_vendor', 'is_staff', 'is_active'
        )

        # Apply pagination
        page_size = 10  # Default page size
        page_number = request.query_params.get('page', 1)
        paginator = Paginator(users, page_size)

        try:
            page = paginator.page(page_number)
        except Exception as e:
            return Response(
                {"error": "Invalid page number."}, status=400
            )

        # Construct response
        response = {
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page.number,
            "results": list(page.object_list)
        }

        return Response(response)
    

class VendorListAPIView(ListAPIView):
    """
    View to list all vendors (admin-only access).
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination