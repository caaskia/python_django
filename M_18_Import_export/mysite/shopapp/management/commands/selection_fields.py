from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo select fields")

        user_info = User.objects.values_list("username", flat=True)
        for u_info in user_info:
            self.stdout.write(f"User {u_info}")

        # product_values = Product.objects.values("pk", "name")
        # for p_values in product_values:
        #     self.stdout.write(f"Product {p_values}")
        self.stdout.write("Done")
