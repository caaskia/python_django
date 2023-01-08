from django.urls import path
from .views import NewsListView, NewsDetailView, NewsCreateFormView, NewsEditFormView

urlpatterns = [
path('news/', NewsListView.as_view(), name ='news'),
path('news/<int:pk>/', NewsDetailView.as_view(), name ='news-detail'),
path('news/create/', NewsCreateFormView.as_view()),
path('news/edit/<int:news_id>/', NewsEditFormView.as_view()),
]

