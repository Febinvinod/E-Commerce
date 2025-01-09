from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import ReviewRating, Product
from .serializers import ReviewRatingSerializer, ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ReviewRatingCreateView(generics.CreateAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']

        # Ensure the user purchased the product before leaving a review
        # Assuming a Purchase model exists; replace this logic as per your application.
        # if not Purchase.objects.filter(user=user, product=product).exists():
        #     raise ValidationError("You can only review products you've purchased.")

        # Ensure the user hasn't already reviewed this product
        if ReviewRating.objects.filter(user=user, product=product).exists():
            raise ValidationError("You have already reviewed this product.")

        serializer.save(user=user)

class ReviewRatingListView(generics.ListAPIView):
    serializer_class = ReviewRatingSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ReviewRating.objects.filter(product_id=product_id)
