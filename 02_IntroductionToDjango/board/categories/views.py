from django.shortcuts import render

def categories(request, *args, **kwargs):

    categories = ['Личные вещи', 'Транспорт', 'Хобби', 'Отдых']

    return render(request, 'categories/categories.html',{'categories': categories})