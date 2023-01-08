from django.db import models

class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(max_length=1000, default='', verbose_name='Содержание')
    active = models.BooleanField(default=True, verbose_name='Флаг активности')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    def __str__(self):
        return self.title

    class Meta:
        # db_table = 'advertisements'
        ordering = ['-created_at']

class Comments(models.Model):
    username = models.CharField(max_length=25, verbose_name='имя пользователя')
    text = models.TextField(max_length=1000, verbose_name='текст комментария')
    news = models.ForeignKey(News,  verbose_name='новость', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text
