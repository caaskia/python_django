from django.shortcuts import render
from django.views.generic import TemplateView

count_views = 0

list_adv = ['Python-фреймворк Django',
                    'Веб-верстка «Базовый уровень',
                    'Система контроля версий Git',
                    'Профессия Python-разработчик',
                    'Профессия Fullstack-разработчик на Python']


class Advertisements(TemplateView):
    template_name = 'advertisements/advertisements.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # global list_adv

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Бесплатные объявления'
        context['name'] = 'Бесплатные объявления в вашем городе'
        # context['description'] = 'Продам магазин Цветы.сад и огород.Площадь 35.7кв.м.Магазин действующий.с выгодной локацией,доступ 24\7,рядом остановка.две школы,продуктовые магазины,удобная ,всем доступная парковка,хорошая клиентская база.Все оборудование и материалы в собственности.В магазине живые срезанные цветы,горшечные растения,горшки,грунты,искусственные цветы и композиции,сувениры,изделия ручной работы,семена'
        context['advertisements'] = list_adv
        return context

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Бесплатные объявления'
        context['name'] = 'Бесплатные объявления в вашем городе'
        context['advertisements'] = list_adv
        context['count_views'] = count_views
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        global count_views
        text = self.request.POST.get("text", "Undefined")
        if text not in ('', "Undefined"):
            list_adv.append(text)

        count_views +=1
        return render(request, 'advertisements/succes.html', {})