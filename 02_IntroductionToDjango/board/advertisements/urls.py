from  django.urls import path
from . import views

urlpatterns = [
path('advertisements/', views.Advertisements.as_view(), name ='advertisements'),
path('advertisements/succes/', views.Advertisements.as_view(), name ='succes'),
]