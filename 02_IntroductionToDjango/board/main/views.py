from django.views.generic import TemplateView


class mainView(TemplateView):
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['categories'] = ['Личные вещи', 'Транспорт', 'Хобби', 'Отдых']
        context['regions'] = ['Витебск', 'Брест', 'Гомель', 'Гродно', 'Могилев']
        return context