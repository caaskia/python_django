# Generated by Django 4.1.6 on 2023-12-03 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_alter_article_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='archived',
        ),
    ]
