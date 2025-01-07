# services.py
import requests
from django.conf import settings

class ProductService:
    @staticmethod
    def get_product(product_id):
        # External API call to get product details
        url = f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Returns product data as a dictionary
        return None
