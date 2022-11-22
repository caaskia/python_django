from  django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path("", views.get_client_ip, name = 'get_client_ip'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)