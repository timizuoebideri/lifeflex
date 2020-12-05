from django.contrib import admin

# Register your models here.
from dashboard.models import Invoice, Withdrawal

admin.site.register(Invoice)
admin.site.register(Withdrawal)
