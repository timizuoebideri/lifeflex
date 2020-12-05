from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    amount = models.CharField(max_length=100)
    purpose = models.CharField(max_length=50)
    method_of_payment = models.CharField(max_length=50, default='None')
    status = models.CharField(max_length=50, default='unpaid')
    comment = models.CharField(max_length=500, default='')
    prove_of_payment = models.ImageField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    amount_requested = models.IntegerField()
    payout_method = models.CharField(max_length=50, default='naira-account')
    comment = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    earning_before = models.IntegerField()
    earning_after = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
