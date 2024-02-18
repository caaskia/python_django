from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db.models import Avg, Count, Max, Min, Sum

from shopapp.models import Product, Order

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk action")

        result = Product.objects.aggregate(
            Avg("price"),
            Max("price"),
            Min("price"),
            Count("id"),
        )
        print(result)

        result = Product.objects.filter(
            name__contains="Smartphone"
            ).aggregate(
            Avg("price"),
            Max("price"),
            min_price=Min("price"),
            count=Count("id"),
        )
        print(result)

        orders = Order.objects.annotate(
            total_price=Sum("products__price", default=0),
            products_count=Count("products"),
        )
        for order in orders:
            print(
                f"Order #{order.id}"
                f" products_count={order.products_count}"
                f" total_price={order.total_price}"
            )

        self.stdout.write("Done")
