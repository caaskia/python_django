# Generated by Django 4.1.6 on 2023-05-15 13:47

from django.db import migrations, models
import shopapp.models


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0010_productimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=shopapp.models.image_preview_directory_path,
            ),
        ),
    ]