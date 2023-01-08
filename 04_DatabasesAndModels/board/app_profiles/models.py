from django.db import models

class User(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=12)
    first_name = models.CharField(max_length=25)
    second_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50)
    birthday = models.DateField(null=True)

    def __str__(self):
        return self.username