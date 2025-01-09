from rest_framework import serializers
from .models import ReviewRating, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ReviewRating
        fields = ['id', 'product', 'user', 'rating', 'review', 'created_at', 'updated_at']
