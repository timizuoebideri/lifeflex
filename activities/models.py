from django.contrib.auth.models import User
from django.core import signals
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from account.models import UserProfile
from dashboard.models import Invoice, Withdrawal


class AccountActivities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    message = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)


def account_created_activity(signal, **kwargs):
    if kwargs['created']:
        AccountActivities.objects.create(
            user=kwargs['instance'],
            type="account",
            message="Your lifeflex account was successfully created",
        )


post_save.connect(account_created_activity, User)


def account_updated_activity(signal, **kwargs):
    if not kwargs['created']:
        AccountActivities.objects.create(
            user=kwargs['instance'].user,
            type="account",
            message="Your account was updated successfully",
        )


post_save.connect(account_updated_activity, UserProfile)


def invoice_created(signal, **kwargs):
    if not kwargs['created']:
        AccountActivities.objects.create(
            user=kwargs['instance'].user,
            type="invoice",
            message=f"An invoice for {kwargs['instance'].purpose} was created"
        )


post_save.connect(invoice_created, Invoice)


def withdrawal_request_created(signal, **kwargs):
    if kwargs['created']:
        AccountActivities.objects.create(
            user=kwargs['instance'].user,
            type=kwargs['instance'].type,
            message=f"Request for withdrawal of ${kwargs['instance'].amount_requested} is been processed"
        )


post_save.connect(withdrawal_request_created, Withdrawal)
