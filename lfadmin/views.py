from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from account.models import UserProfile
from activities.models import AccountActivities
from dashboard.models import Invoice, Withdrawal


class AdminDashboard(TemplateView):
    template_name = 'lfadmin/dashboard.html'

    def get(self, request):
        users = User.objects.count()
        invoices = Invoice.objects.count()

        args = {
            'users': users,
            'invoice': invoices
        }

        return render(request, self.template_name, args)


class UsersView(ListView):
    template_name = 'lfadmin/users.html'
    ordering = '-id'
    model = User
    paginate_by = 10
    context_object_name = 'users'


class UserSingleView(TemplateView):
    template_name = 'lfadmin/users-view.html'

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        invoice = Invoice.objects.filter(user=user)
        withdrawals = Withdrawal.objects.filter(user=user)
        args = {
            'user': user,
            'invoices': invoice,
            'withdrawals': withdrawals
        }
        return render(request, self.template_name, args)


class InvoiceView(ListView):
    model = Invoice
    ordering = '-date_updated'
    paginate_by = 10
    template_name = 'lfadmin/invoices.html'
    context_object_name = 'invoices'


def invoiceSingleView(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    if request.method == 'GET':
        args = {'invoice': invoice}
        return render(request, 'lfadmin/invoice-view.html', args)
    else:
        Invoice.objects.filter(pk=pk).update(comment=request.POST['comment'], status=request.POST['status'])
        AccountActivities(
            user=invoice.user,
            type='invoice',
            message=f"Your Invoice #{pk} has been {request.POST['status']}."
        ).save()
        if request.POST['status'] == 'approve':
            UserProfile.objects.filter(pk=invoice.user.userprofile.pk).update(account_balance=invoice.amount)
            AccountActivities(
                user=invoice.user,
                type='credit',
                message=f"Your Account has been credited with ${invoice.amount}."
            ).save()

        return redirect(reverse('admin-all-invoice'))


class WithdrawalView(ListView):
    # model = Withdrawal
    template_name = 'lfadmin/withdrawal.html'

    def get(self, request):
        model = Withdrawal.objects.all().order_by('-date_updated')
        args={
            'withdrawals': model
        }
        return render(request, self.template_name, args)


def withdrawalSingleView(request, pk):
    model = Withdrawal.objects.get(pk=pk)

    if request.method == 'GET':
        args = {'withdrawal': model}
        return render(request, 'lfadmin/Withdrawal-view.html', args)
    else:
        Withdrawal.objects.filter(pk=pk).update(comment=request.POST['comment'], status=request.POST['status'])
        AccountActivities(
            user=model.user,
            type='withdrawal',
            message=f"Your Withdrawal Request for ${model.amount_requested} has been {request.POST['status']}."
        ).save()
        if request.POST['status'] == 'approved':
            UserProfile.objects.filter(pk=model.user.userprofile.pk).update(earning_balance=model.earning_after)
            AccountActivities(
                user=model.user,
                type='credit',
                message=f"Your Earning Account has been debited with a sum of ${model.amount_requested}."
            ).save()

        return redirect(reverse('admin-all-withdrawals'))
