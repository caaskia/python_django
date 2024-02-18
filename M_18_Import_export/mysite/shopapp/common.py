from csv import DictReader
from io import TextIOWrapper

# from M_18_Import_export.mysite.shopapp.models import Product
from shopapp.models import Product


def save_csv_products(file, encoding="utf-8"):
    csv_file = TextIOWrapper(file, encoding=encoding)
    reader = DictReader(csv_file)

    products = [
        Product(**row) for row in reader
    ]

    Product.objects.bulk_create(products)
    return products
