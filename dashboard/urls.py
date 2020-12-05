from django.urls import path

from .views import dashboard, withdrawal, account_activity, invoice, invoice_view

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('withdrawal/', withdrawal, name='withdrawal'),

    path('invoice/', invoice, name='invoice'),
    path('invoice/<pk>/view/', invoice_view, name='invoice-view'),

    path('account-activity/', account_activity, name='account-activity'),
]