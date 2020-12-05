from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
# Create your views here.

from account.forms import ActivityFilterForm
from activities.models import AccountActivities
from dashboard.models import Invoice, Withdrawal


def dashboard(request):
    activities = AccountActivities.objects.filter(user=request.user).order_by('-date')[:5]
    args = {
        'activities': activities,
    }
    return render(request, 'dashboard/dashboard.html', args)


def withdrawal(request):
    # Withdrawal.objects.all().delete()
    if request.method == 'GET':
        withdraw = Withdrawal.objects.filter(user=request.user).order_by('-date_updated')
        args = {'withdraws': withdraw, 'withdraw_single': None}
        if 'withdraw_id' in request.GET:
            withdraw_single = Withdrawal.objects.get(pk=request.GET['withdraw_id'])
            args = {'withdraws': withdraw, 'withdraw_single': withdraw_single}
        return render(request, 'dashboard/withdrawal.html', args)
    else:
        bal = request.user.userprofile.earning_balance
        new_bal = float(bal) - float(request.POST['amount'])

        withdraw = Withdrawal(
            user=request.user,
            type='withdrawal',
            amount_requested=request.POST['amount'],
            payout_method=request.POST['payout-method'],
            earning_before=bal,
            earning_after=new_bal,
            status='processing'
        ).save()
        # messages.INFO(request, messages.INFO('Hello'), extra_tags='calm')
        return redirect(reverse('withdrawal'))


def invoice(request):
    inv = Invoice.objects.filter(user=request.user).order_by('-id')
    pag = Paginator(inv, 10)
    if 'pg' in request.GET:
        page = request.GET['pg']
    else:
        page = 1
    pg = pag.page(page)
    args = {
        'invoice': pg
    }
    return render(request, 'dashboard/invoice.html', args)


def invoice_view(request, pk):
    inv = Invoice.objects.get(pk=pk)
    if request.method == 'GET':
        args = {'invoice': inv}
        return render(request, 'dashboard/invoice-view.html', args)
    else:
        Invoice.objects.filter(pk=pk).update(status='processing', method_of_payment=request.POST['method_of_payment'])
        AccountActivities(
            user=request.user,
            type='invoice',
            message=f"Invoice #{inv.id} is been processed"
        ).save()
        return redirect(reverse('invoice'))


def account_activity(request):
    activity = AccountActivities.objects.filter(user=request.user).order_by('-date')
    activity_filter = ActivityFilterForm(request.GET, queryset=activity)
    activity = activity_filter.qs
    if 'pg' in request.GET:
        pg = request.GET['pg']
    else:
        pg = 1
    activity = Paginator(activity, 10).page(pg)

    args = {'activity': activity, 'filter': activity_filter}
    return render(request, 'dashboard/account-activity.html', args)
