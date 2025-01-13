from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.db.models import Sum, Count,F
from django.db.models import Q,Prefetch
from rest_framework.permissions import IsAuthenticated
from accounts.models import *

class ProductTypeListAPIView(ListAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

# View for categories
class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk=None):
        """
        Handle both listing all products and retrieving a specific product by ID.
        """
        if pk:  # If `pk` is provided, get a specific product
            product = self.get_product(pk)
            if product:
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # List all products of the authenticated vendor
        vendor = request.user.vendor_profile  # Get the authenticated vendor
        products = Product.objects.filter(vendor=vendor)

        # Optional filters
        name = request.query_params.get('name', None)
        if name:
            products = products.filter(name__icontains=name)

        brand = request.query_params.get('brand', None)
        if brand:
            products = products.filter(brand__icontains=brand)

        category = request.query_params.get('category', None)
        if category:
            products = products.filter(category__name__icontains=category)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new product associated with the authenticated vendor.
        """
        user = request.user

        # Check if the user has an associated vendor profile
        try:
            vendor = Vendor.objects.get(user=user)  # Fetch the vendor linked to the logged-in user
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor profile not found for the authenticated user.'}, status=status.HTTP_404_NOT_FOUND)

        # Pass the request context to the serializer
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # The vendor is automatically associated in the serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update a specific product.
        """
        product = self.get_product(pk)
        if product:
            serializer = ProductSerializer(product, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        """
        Partially update a specific product.
        """
        product = self.get_product(pk)
        if product:
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """
        Delete a specific product.
        """
        product = self.get_product(pk)
        if product:
            product.delete()
            return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None
        
class ProductAttributeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,):
        attributes = ProductAttribute.objects.all()
        serializer = ProductAttributeSerializer(attributes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductAttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for attribute values
class AttributeValueAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, attribute_id=None):
        if attribute_id:
            values = AttributeValue.objects.filter(attribute_id=attribute_id)
        else:
            values = AttributeValue.objects.all()
        serializer = AttributeValueSerializer(values, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AttributeValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        try:
            value = AttributeValue.objects.get(pk=pk)
            value.delete()
            return Response({'message': 'Value deleted'}, status=status.HTTP_204_NO_CONTENT)
        except AttributeValue.DoesNotExist:
            return Response({'error': 'Value not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class ProductSearchAPIView(APIView):
    def post(self, request):
        # Extract search criteria from the request body (raw JSON)
        search_params = request.data.get("search", {})

        # Initialize the queryset
        products = Product.objects.all()

        # Apply filters if search criteria are provided
        name = search_params.get('name', None)
        brand = search_params.get('brand', None)
        min_price = search_params.get('min_price', None)
        max_price = search_params.get('max_price', None)
        rating = search_params.get('rating', None)
        category = search_params.get('category', None)
        color = search_params.get('color', None)  # Color filter

        try:
            # Name filter
            if name:
                products = products.filter(name__icontains=name)

            # Brand filter
            if brand:
                products = products.filter(brand__icontains=brand)

            # Category filter
            if category:
                products = products.filter(category__name__icontains=category)

            # Price range filter
            if min_price:
                products = products.filter(price__gte=float(min_price))
            if max_price:
                products = products.filter(price__lte=float(max_price))

            # Rating filter
            if rating:
                products = products.filter(rating__gte=float(rating))

            # Color filter
            if color:
                products = products.filter(
                    Q(attributes__key='Color') & Q(attributes__values__value=color)
                )

            # If no products are found
            if not products.exists():
                return Response(
                    {"detail": "No products found with the given criteria."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Serialize the filtered products
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": f"Invalid filter value: {e}"}, status=status.HTTP_400_BAD_REQUEST
            )
    

class ProductAnalyticsAPIView(APIView):
    def get(self):
        # Total sales per product
        total_sales = Product.objects.annotate(
            total_sales=Sum('sale__quantity')
        ).values('id', 'name', 'total_sales').order_by('-total_sales')

        # Top-selling products
        top_selling = Product.objects.annotate(
            total_sales=Sum('sale__quantity')
        ).values('id', 'name', 'total_sales').order_by('-total_sales')[:10]

        # Low stock products
        low_stock = Product.objects.filter(inventory__lte=10).values('id', 'name', 'inventory')

        # Average product rating
        product_ratings = Product.objects.annotate(
            average_rating=Sum('review__rating') / Count('review')
        ).values('id', 'name', 'average_rating')

        # Sales per vendor
        vendor_sales = Sale.objects.values('vendor__id').annotate( # type: ignore
            total_sales=Sum('quantity')
        ).values('vendor__id', 'total_sales')

        # Combine all the reports into one response
        analytics_data = {
            'total_sales_per_product': total_sales,
            'top_selling_products': top_selling,
            'low_stock_products': low_stock,
            'average_product_rating': product_ratings,
            'sales_per_vendor': vendor_sales
        }

        return Response(analytics_data, status=status.HTTP_200_OK)
    

class VendorDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Aggregate data for all vendors
        # Total sales (quantity of products sold)
        total_sales = Order.objects.filter(status='completed').aggregate(
            total=Sum('quantity')
        )['total'] or 0

        # Total earnings
        total_earnings = Order.objects.filter(status='completed').aggregate(
            earnings=Sum('total_price')
        )['earnings'] or 0

        # Admin's total commission
        total_admin_earnings = Order.objects.filter(status='completed').aggregate(
            admin_earnings=Sum(F('total_price') * F('product__commission_rate') / 100)
        )['admin_earnings'] or 0

        # Vendor's total earnings (platform earnings - admin's share)
        total_vendor_earnings = total_earnings - total_admin_earnings

        # Recent orders
        recent_orders = Order.objects.all().order_by('-created_at')[:5]
        recent_orders_data = [
            {
                "order_id": order.id,
                "product": order.product.name,
                "quantity": order.quantity,
                "total_price": order.total_price,
                "admin_earnings": order.admin_earnings,
                "vendor_earnings": order.vendor_earnings,
                "status": order.status,
                "date": order.created_at,
            }
            for order in recent_orders
        ]

        # Response data
        dashboard_data = {
            "total_sales": total_sales,
            "total_earnings": total_earnings,
            "total_admin_earnings": total_admin_earnings,
            "total_vendor_earnings": total_vendor_earnings,
            "recent_orders": recent_orders_data,
        }
        return Response(dashboard_data)

    
class AllCategoriesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.prefetch_related(
        Prefetch('attributes__values')
    ).all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Custom filtering logic for products.
        Filters by category, price, and attribute values strictly.
        """
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        price = self.request.query_params.get('price')
        value = self.request.query_params.get('value')

        # Filtering by category
        if category:
            queryset = queryset.filter(category=category)

        # Filtering by nested attribute price
        if price:
            queryset = queryset.filter(
                attributes__values__price=price
            ).distinct()

        # Filtering by nested attribute value
        if value:
            queryset = queryset.filter(
                attributes__values__value=value
            ).distinct()

        return queryset

    
class JSONSearchAPIView(APIView):
    def post(self, request):
        search_params = request.data.get("search", {})
        products = Product.objects.all()

        # Apply filters dynamically
        if 'name' in search_params:
            products = products.filter(name__icontains=search_params['name'])
        if 'brand' in search_params:
            products = products.filter(brand__icontains=search_params['brand'])
        if 'category' in search_params:
            products = products.filter(category__name__icontains=search_params['category'])
        if 'min_price' in search_params:
            products = products.filter(price__gte=search_params['min_price'])
        if 'max_price' in search_params:
            products = products.filter(price__lte=search_params['max_price'])

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

        profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

        profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
