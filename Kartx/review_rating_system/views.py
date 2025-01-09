from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import ReviewRating, Product
from .serializers import ReviewRatingSerializer, ProductSerializer

# View for listing all products
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# View to allow authenticated users to create reviews and ratings
class ReviewRatingCreateView(generics.CreateAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
    permission_class = []
    # permission_classes = [permissions.IsAuthenticated] 
     # Only authenticated users can post a review

    def perform_create(self, serializer):
        user = self.request.user  # Get the currently logged-in user
        product = serializer.validated_data['product']  # Get the product for the review

        # Check if the user has already reviewed this product
        if ReviewRating.objects.filter(user=user, product=product).exists():
            raise ValidationError("You have already reviewed this product.")

        # Save the review with the user who created it
        serializer.save(user=user)

# View to list all reviews for a specific product
class ReviewRatingListView(generics.ListAPIView):
    serializer_class = ReviewRatingSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ReviewRating.objects.filter(product_id=product_id)
