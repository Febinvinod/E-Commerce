from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from accounts.models import*
from catalog.serializers import *
from accounts.models import *
from accounts.serializers import *


# Custom permission for admin-only access
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff



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

    def put(self, request, pk=None):
        """
        Update user details.
        """
        if not pk:
            return Response(
                {"error": "User ID (pk) is required for update."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)  # Use `partial=True` for partial updates
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class VendorAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Vendor.objects.all()
        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
    # Create a new user
     serializer = UserSerializer(data=request.data, partial=True)
     serializer.is_valid(raise_exception=True)

    # Save the user instance
     user = serializer.save()

    # Set the is_vendor field to True and save again
     user.is_vendor = True
     user.save()

     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        """
        Update vendor details.
        """
        if not pk:
            return Response(
                {"error": "Vendor ID (pk) is required for update."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        vendor = get_object_or_404(User, pk=pk, is_vendor=True)
        serializer = UserSerializer(vendor, data=request.data, partial=True)  # Use `partial=True` for partial updates
        serializer.is_valid(raise_exception=True)
        serializer.save()

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

class ApproveVendorView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            vendor = Vendor.objects.get(pk=pk)
            if vendor.approved:
                return Response({'message': 'Vendor is already approved.'}, status=status.HTTP_400_BAD_REQUEST)
            
            vendor.approved = True
            vendor.save()
            return Response({'message': 'Vendor approved successfully.'}, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class PendingVendorsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        pending_vendors = Vendor.objects.filter(approved=False)
        serializer = VendorSerializer(pending_vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)