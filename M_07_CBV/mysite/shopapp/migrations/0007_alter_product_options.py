# Generated by Django 4.1.5 on 2023-01-21 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0006_order_products"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["name", "price"]},
        ),
    ]