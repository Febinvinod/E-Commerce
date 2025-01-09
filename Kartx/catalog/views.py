from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.db.models import Sum, Count

class ProductTypeListAPIView(ListAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

# View for categories
class CategoryAPIView(APIView):
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


# View for products
class ProductAPIView(APIView):
    def get(self,):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get_product_with_attributes(self, pk):
        product = self.get_product(pk)
        if product:
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    def put(self, request, pk=None):
        product = self.get_product(pk)
        if product:
            serializer = ProductSerializer(product, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk=None):
        product = self.get_product(pk)
        if product:
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk=None):
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
        
    def get(self, request):
        products = Product.objects.all()

        # Filter by product name if provided in query parameters
        name = request.query_params.get('name', None)
        if name:
            products = products.filter(name__icontains=name)
            
        brand = request.query_params.get('brand', None)
        if brand:
            products = products.filter(brand__icontains=brand)

        # Filter by product type if provided in query parameters
        category = request.query_params.get('category', None)  # Using category for product type
        if category:
            products = products.filter(product_type__name=category)

        # Additional filters can go here, like filtering by brand, price, rating, etc.
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# View for product attributes
class ProductAttributeAPIView(APIView):
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
        # Extract the search criteria from the request body (raw JSON)
        search_params = request.data.get("search", {})

        # Initialize the queryset
        products = Product.objects.all()

        # Apply filters only if the search term is provided and not empty
        name = search_params.get('name', None)
        brand = search_params.get('brand', None)
        min_price = search_params.get('min_price', None)
        max_price = search_params.get('max_price', None)
        rating = search_params.get('rating', None)
        category = search_params.get('category', None)
        color = search_params.get('color', None)  # Filter by color attribute (if any)

        # If 'name' is provided and not empty, filter by product name
        if name:
            products = products.filter(name__icontains=name)

        # Apply additional filters if provided
        if brand:
            products = products.filter(brand__icontains=brand)
        if category:
            products = products.filter(category__name__icontains=category)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if rating:
            products = products.filter(rating__gte=rating)

        # Filter products by color (if provided as a search parameter)
        if color:
            products = products.filter(attributes__key='Color', attributes__values__value=color)

        # If no filters are applied, return an empty response or all products
        if not products.exists():
            return Response({"detail": "No products found with the given criteria."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the filtered products
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

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
    def get(self, request):
        # Get the vendor_id from query parameters
        vendor_id = request.query_params.get('vendor_id')
        if not vendor_id:
            return Response({"error": "vendor_id is required"}, status=400)

        try:
            # Convert vendor_id to an integer
            vendor_id = int(vendor_id)
        except ValueError:
            return Response({"error": "Invalid vendor_id. Must be an integer."}, status=400)

        # Total sales (quantity of products sold)
        total_sales = Order.objects.filter(vendor_id=vendor_id, status='completed').aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

        # Total earnings
        total_earnings = Order.objects.filter(vendor_id=vendor_id, status='completed').aggregate(
            earnings=models.Sum('total_price')
        )['earnings'] or 0

        # Recent orders
        recent_orders = Order.objects.filter(vendor_id=vendor_id).order_by('-created_at')[:5]
        recent_orders_data = [
            {
                "order_id": order.id,
                "product": order.product.name,
                "quantity": order.quantity,
                "total_price": order.total_price,
                "status": order.status,
                "date": order.created_at,
            }
            for order in recent_orders
        ]

        # Response data
        dashboard_data = {
            "total_sales": total_sales,
            "total_earnings": total_earnings,
            "recent_orders": recent_orders_data,
        }
        return Response(dashboard_data)

    
class AllCategoriesAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductListingAPIView(APIView):
    def get(self):
        products = Product.objects.prefetch_related('attributes__values').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
    permission_classes = []

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
