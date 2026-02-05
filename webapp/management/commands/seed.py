from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal

from webapp.models import Category, Product, Store, Inventory


class Command(BaseCommand):

    help = "Generate dummy ecommerce data"


    def handle(self, *args, **kwargs):

        fake = Faker()

        self.stdout.write("Starting database seeding...")


        # -----------------------------
        # Clear Old Data
        # -----------------------------
        Inventory.objects.all().delete()
        Product.objects.all().delete()
        Store.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Old data cleared")


        # -----------------------------
        # Categories (Safe Method)
        # -----------------------------
        CATEGORY_NAMES = [
            "Electronics", "Clothing", "Books", "Home",
            "Sports", "Beauty", "Toys", "Grocery",
            "Furniture", "Automobile", "Health", "Office"
        ]

        categories = []

        for name in CATEGORY_NAMES:

            cat = Category.objects.create(name=name)
            categories.append(cat)

        self.stdout.write(f"Categories created: {len(categories)}")


        # -----------------------------
        # Stores
        # -----------------------------
        stores = []

        for _ in range(20):

            store = Store.objects.create(
                name=fake.company(),
                location=fake.city()
            )

            stores.append(store)

        self.stdout.write(f"Stores created: {len(stores)}")


        # -----------------------------
        # Products
        # -----------------------------
        BASE_PRODUCTS = [
            "Laptop", "Phone", "Tablet", "Headphones",
            "Mouse", "Keyboard", "Monitor", "Camera",
            "Speaker", "Printer", "Watch", "Charger"
        ]
        DESCRIPTION_TEMPLATES = [
    "High-quality {name} designed for everyday use.",
    "Durable and reliable {name} with modern features.",
    "Premium {name} suitable for home and office.",
    "Compact and lightweight {name} for easy handling.",
    "Affordable {name} with excellent performance.",
    "Advanced {name} built with long-lasting materials.",
]


        products = []

        for i in range(1000):

            base = random.choice(BASE_PRODUCTS)

            title = f"{base} {fake.random_int(100,999)}"
            description = random.choice(DESCRIPTION_TEMPLATES).format(
        name=base
    )

            product = Product.objects.create(
                title=title,
                description=description,
                price=Decimal(random.randint(500, 50000)),
                category=random.choice(categories)
            )

            products.append(product)

            if i % 100 == 0:
                self.stdout.write(f"{i} products created...")

        self.stdout.write(f"Products created: {len(products)}")


        # -----------------------------
        # Inventory
        # -----------------------------
        inventory_count = 0

        for store in stores:

            selected_products = random.sample(products, 300)

            for prod in selected_products:

                Inventory.objects.create(
                    store=store,
                    product=prod,
                    quantity=random.randint(0, 100)
                )

                inventory_count += 1

        self.stdout.write(f"Inventory created: {inventory_count}")


        self.stdout.write(
            self.style.SUCCESS("Database seeding completed successfully!")
        )
