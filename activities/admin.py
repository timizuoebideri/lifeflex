from django.contrib import admin

# Register your models here.
from activities.models import AccountActivities


class AccountActivitiesAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'message']


admin.site.register(AccountActivities, AccountActivitiesAdmin)
