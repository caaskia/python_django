from django.shortcuts import render
from django.views.generic import ListView, DetailView

from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormMixin

from .models import News, Comments
from .forms import NewsForm, CommentsForm


class NewsListView(ListView):
    model = News
    # template_name = 'app_news/news_list.html'
    # queryset = Advertisement.objects.all()[:5]
    context_object_name = 'news_list'

class NewsDetailView(DetailView, FormMixin):
# class NewsDetailView(DetailView):
    model = News
    context_object_name = 'news'
    form_class = CommentsForm

    def get_object(self, queryset=None):
        self.item = super().get_object(queryset)
        # self.item.views_count += 1
        # self.item.save()
        return self.item
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments_list = self.item.comments.all()
        context['comments_list'] = comments_list
        context['user_form'] = self.form_class
        return context

    def post(self, request,  *args, **kwargs):
        user_form = CommentsForm(request.POST)

        news_id = kwargs['pk']

        if user_form.is_valid():
            cleaned_data = user_form.cleaned_data
            post = News.objects.get(id__exact=news_id)
            text = Comments(username=cleaned_data['username'], text=cleaned_data['text'], news=post)
            text.save()

            # Comments.objects.create(**user_form.cleaned_data)
            # Comments.objects.create(cleaned_data)

        return HttpResponseRedirect(f'/news/{news_id}/')
        # return render(request, 'app_news/news_create.html', context={'user_form': user_form})
        # return render(request, 'app_news/news_detail.html', context={'user_form': user_form, 'news_id': news_id})


class NewsCreateFormView(View):

    def get(self, request):
        user_form = NewsForm()
        return render(request, 'app_news/news_create.html', context={'user_form': user_form})

    def post(self, request):
        user_form = NewsForm(request.POST)

        if user_form.is_valid():
            News.objects.create(**user_form.cleaned_data)
            return HttpResponseRedirect('/news/')
        return render(request, 'app_news/news_create.html', context={'user_form': user_form})

class NewsEditFormView(View):

    def get(self, request, news_id):
        user = News.objects.get(id = news_id)
        user_form = NewsForm(instance = user)
        return render(request, 'app_news/news_edit.html', context={'user_form': user_form, 'news_id': news_id})

    def post(self, request, news_id):
        user = News.objects.get(id = news_id)
        user_form = NewsForm(request.POST, instance = user)

        if user_form.is_valid():
            user.save()
        return render(request, 'app_news/news_edit.html', context={'user_form': user_form, 'news_id': news_id})



