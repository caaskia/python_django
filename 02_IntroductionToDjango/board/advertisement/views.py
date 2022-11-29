from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic import TemplateView


def advertisements_list(request, *args, **kwargs):
    advertisements = ['Python-фреймворк Django',
                      'Веб-верстка «Базовый уровень',
                      'Система контроля версий Git',
                      'Профессия Python-разработчик',
                      'Профессия Fullstack-разработчик на Python']

    return render(request, 'advertisement/advertisements_list.html',{'advertisements': advertisements})


def advertisement01(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement01.html',{})

def advertisement02(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement02.html',{})

def advertisement03(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement03.html',{})

def advertisement04(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement04.html',{})

def advertisement05(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement05.html',{})

# def About(request, *args, **kwargs):
#     title = 'Бесплатные объявления'
#     name = 'Бесплатные объявления в вашем городе'
#     return render(request, 'advertisement/about.html',{'title': title, 'name': name})

# class AboutView(TemplateView):
#     template_name = 'advertisement/about.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Бесплатные объявления'
#         context['name'] = 'Бесплатные объявления в вашем городе'
#         context['description'] = 'Продам магазин Цветы.сад и огород.Площадь 35.7кв.м.Магазин действующий.с выгодной локацией,доступ 24\7,рядом остановка.две школы,продуктовые магазины,удобная ,всем доступная парковка,хорошая клиентская база.Все оборудование и материалы в собственности.В магазине живые срезанные цветы,горшечные растения,горшки,грунты,искусственные цветы и композиции,сувениры,изделия ручной работы,семена'
#         return context



