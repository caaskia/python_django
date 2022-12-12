from django.urls import path
from .views import AdvertisementsListView, AdvertisementsDetailView

urlpatterns = [
path('advertisements/', AdvertisementsListView.as_view(), name ='advertisements'),
path('advertisements/<int:pk>', AdvertisementsDetailView.as_view(), name ='advertisements-detail'),
]

