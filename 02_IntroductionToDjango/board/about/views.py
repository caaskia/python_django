# from django.shortcuts import render
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'about/about.html'
    # template_name = 'advertisement/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Бесплатные объявления'
        context['name'] = 'Бесплатные объявления в вашем городе'
        context['description'] = 'Размещаем объявления на любые темы. Пользуйтесь нашей доской объявлений. Извлекайте бесплатно выгоду!'
        return context
