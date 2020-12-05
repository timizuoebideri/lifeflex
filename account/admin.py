from django.contrib import admin

# Register your models here.
from .models import UserProfile

class AdPro(admin.ModelAdmin):
    list_display = ['user', 'account_type']

admin.site.register(UserProfile, AdPro)
