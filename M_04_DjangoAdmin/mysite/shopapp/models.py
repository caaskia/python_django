from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):

    class Meta:
        # db_table = 'product'
        ordering = ['name', 'price']

    name = models.CharField(max_length=100, verbose_name='имя')
    description = models.TextField(null=False, blank=True, verbose_name='описание')
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='цена')
    discount = models.SmallIntegerField(default=0, verbose_name='скидка')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archivied = models.BooleanField(default=False)

    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 48:
    #         return str(self.description)
    #     return self.description[:48] + '...'


    def __str__(self) -> str:
        return f'{self.pk}. {self.name!r}({self.price})'


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")


