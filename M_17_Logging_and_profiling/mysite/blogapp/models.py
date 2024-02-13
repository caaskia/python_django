from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=False, blank=True)

    def __str__(self):
        # return f"Author(pk={self.pk}, name={self.name!r})"
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        # return f"Category(pk={self.pk}, name={self.name!r})"
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        # return f"Tag(pk={self.pk}, name={self.name!r})"
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="articles")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles")
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")

    def __str__(self):
        # return f"Article(pk={self.pk}, title={self.title!r})"
        return self.title
