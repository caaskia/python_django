from django.views.generic import ListView

from .models import Article


class BlogListView(ListView):
    template_name = "blogapp/article_list.html"
    model = Article
    context_object_name = "articles"
    queryset = Article.objects.select_related("author", "category").prefetch_related("tags")
