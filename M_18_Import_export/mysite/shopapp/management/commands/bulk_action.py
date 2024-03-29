from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk action")

        result = Product.objects.filter(
            name__contains="Smartphone"
        ).update(discount=10)
        print(result)

        # info = [
        #     ('Smartphone1', 199),
        #     ('Smartphone2', 299),
        #     ('Smartphone3', 399),
        # ]
        #
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        #
        # result = Product.objects.bulk_create(products)
        #
        # for obj in result:
        #     self.stdout.write(f"Product {obj}")

        self.stdout.write("Done")
