from django.http import HttpResponse

from django.views import View


class ToDoView(View):

    def get(self, request, *args, **kwargs):
        todo_set = {'Установить python',
                    'Установить django',
                    'Запустить сервер',
                    'Порадоваться результату',
                    'Еще задание'}

        todo_dict = dict.fromkeys(todo_set, 0)  # Dict хранит данные в случайном порядке

        resp = [f'<li>{key}</li>' for key in todo_dict]
        resp.insert(0, '<ul>')
        resp.append('</ul>')

        return HttpResponse(resp)

        # return HttpResponse('<ul>'
        #                     '<li>Установить python</li>'
        #                     '<li>Установить django</li>'
        #                     '<li>Запустить сервер</li>'
        #                     '<li>Порадоваться результату</li>'
        #                     '</ul>')
