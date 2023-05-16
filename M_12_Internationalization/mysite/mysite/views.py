from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "items": 1,
        }
        return render(request, 'mysite/index.html', context=context)