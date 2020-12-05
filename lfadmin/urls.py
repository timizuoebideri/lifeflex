from django.urls import path

from .views import AdminDashboard, UsersView, UserSingleView, InvoiceView, invoiceSingleView, WithdrawalView, \
    withdrawalSingleView

urlpatterns = [
    path('', AdminDashboard.as_view(), name='admin-dashboard'),
    path('users/', UsersView.as_view(), name='admin-all-users'),
    path('users/<pk>/view', UserSingleView.as_view(), name='admin-single-users'),

    path('invoices/', InvoiceView.as_view(), name='admin-all-invoice'),
    path('invoices/<pk>/', invoiceSingleView, name='admin-single-invoice'),

    path('withdawal/', WithdrawalView.as_view(), name='admin-all-withdrawals'),
    path('withdawal/<pk>/', withdrawalSingleView, name='admin-single-withdrawal'),

]