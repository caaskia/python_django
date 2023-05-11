from django.contrib import admin

from .models import Profile

# admin.site.register(Profile)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = "bio", "agreement_accepted", "user_id", "avatar"
    list_display_links =  "bio", "user_id"
    ordering = "user_id",