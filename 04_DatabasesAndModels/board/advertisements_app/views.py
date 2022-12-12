# from django.shortcuts import render
from django.views.generic import ListView, DetailView

from  .models import Advertisement

class AdvertisementsListView(ListView):
    model = Advertisement
    template_name = 'advertisements/advertisements_list.html'
    context_object_name = 'advertisements'
    # queryset = Advertisement.objects.all()[:5]

class AdvertisementsDetailView(DetailView):
    model = Advertisement
    context_object_name = 'advertisement'

    def get_object(self, queryset=None):
        self.item = super().get_object(queryset)
        self.item.views_count += 1
        self.item.save()
        return self.item

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        # queryset = super().get_queryset(*args, **kwargs)
        # item = super().get_object(queryset)
        price = self.item.price
        context['сurrency'] = round(price / 62.3918, 2)
        return context

    # def get_queryset(self, *args, **kwargs):
    #     # qset = super(AdvertisementsDetailView, self).get_queryset(*args, **kwargs)
    #     queryset = super().get_queryset(*args, **kwargs)
    #     item = super().get_object(queryset)
    #     сurrency = item.price / 62.3918
    #     return queryset.annotate(сurrency)




