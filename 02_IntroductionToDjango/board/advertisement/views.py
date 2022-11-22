from django.shortcuts import render
from django.http import HttpResponse


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

