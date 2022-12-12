from django.contrib import admin
from .models import Advertisement, AdvertisementStatus, AdvertisementRubric, AdvertisementTypes, Publisher
# Register your models here.

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass

@admin.register(AdvertisementStatus)
class AdvertisementStatusAdmin(admin.ModelAdmin):
    pass

@admin.register(AdvertisementRubric)
class AdvertisementRubricAdmin(admin.ModelAdmin):
    pass

@admin.register(AdvertisementTypes)
class AdvertisementTypes(admin.ModelAdmin):
    pass

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass