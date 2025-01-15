import random
from faker import Faker
from django.core.management.base import BaseCommand
from catalog.models import Product, Category
from accounts.models import Vendor

class Command(BaseCommand):
    help = 'Seed the database with bulk products'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Ensure you have vendors and categories in the database
        vendors = list(Vendor.objects.all())
        categories = list(Category.objects.all())

        if not vendors or not categories:
            self.stdout.write(self.style.ERROR("Please add some vendors and categories before seeding products."))
            return

        product_list = []

        for _ in range(100):  # Number of products to create
            product_list.append(
                Product(
                    vendor=random.choice(vendors),
                    name=fake.unique.word().capitalize(),
                    description=fake.text(max_nb_chars=200),
                    inventory=random.randint(1, 500),
                    category=random.choice(categories),
                    brand=fake.company(),
                    rating=round(random.uniform(0, 5), 1),
                )
            )

        Product.objects.bulk_create(product_list)

        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(product_list)} products!'))
