from django.db import models

class Advertisement(models.Model):
    title = models.CharField(max_length=1000, verbose_name='Заголовок')
    description = models.CharField(max_length=1000, default='', verbose_name='описание')
    price = models.FloatField(verbose_name='цена', default=0)
    # views_count = models.IntegerField(verbose_name='количество просмотров', default=0)
    views_count = models.PositiveIntegerField(verbose_name='количество просмотров', default=0)
    public_date_start = models.DateTimeField(auto_now_add=True)
    public_date_end = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('AdvertisementStatus', default=None, null=True, on_delete=models.CASCADE,
                               verbose_name='статус', related_name='advertisements')
    type = models.ForeignKey('AdvertisementTypes', default=None, null=True, on_delete=models.CASCADE,
                             verbose_name='тип', related_name='advertisements')
    rubric = models.ForeignKey('AdvertisementRubric', default=None, null=True, on_delete=models.CASCADE,
                               verbose_name='рубрика', related_name='advertisements')
    publisher = models.ForeignKey('Publisher', default=None, null=True, on_delete=models.CASCADE,
                               verbose_name='автор', related_name='advertisements')

    def __str__(self):
        return self.title

    class Meta:
        # db_table = 'advertisements'
        ordering = ['title']

class AdvertisementStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AdvertisementTypes(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AdvertisementRubric(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=50)
    # phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.name

