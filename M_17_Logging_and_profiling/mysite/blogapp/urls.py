from django.urls import path, include

from .views import (
    BlogListView
)

app_name = "blogapp"


urlpatterns = [
    path("articles/", BlogListView.as_view(), name="articles_list"),
]
