from  django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path("", views.advertisements_list, name ='advertisements_list'),
path("advertisement01", views.advertisement01, name ='advertisement01'),
path("advertisement02", views.advertisement02, name ='advertisement02'),
path("advertisement03", views.advertisement03, name ='advertisement03'),
path("advertisement04", views.advertisement04, name ='advertisement04'),
path("advertisement05", views.advertisement05, name ='advertisement05'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)