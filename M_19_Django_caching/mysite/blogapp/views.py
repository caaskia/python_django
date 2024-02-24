from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView

from .models import Article


class ArticleListView(ListView):
    queryset = (Article.objects
                .filter(published_at__isnull=False)
                .order_by("-published_at"))
    # template_name = "blogapp/article_list.html"


class ArticleDetailView(DetailView):
    model = Article
    # template_name = "blogapp/article_detail.html"


class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "New posts of my blog."
    link = reverse_lazy("blogapp:articles")

    def items(self):
        return (Article.objects
                .filter(published_at__isnull=False)
                .order_by('-published_at')[:5]
                )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body[:200]

    # def item_link(self, item):
    #     return reverse("blogapp:article", kwargs={"pk": item.pk})
