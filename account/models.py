from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200, default='', blank=True, null=True)
    bank_account_number = models.IntegerField( default=0, blank=True, null=True)
    bitcoin_wallet = models.CharField(max_length=200, default='', blank=True, null=True)
    account_type = models.CharField(default='None', max_length=50)
    image = models.ImageField(null=True, blank=True)
    account_balance = models.IntegerField(default=0)
    earning_balance = models.FloatField(default=0)
    active = models.CharField(max_length=50, default='False')
    total_withdrawal = models.IntegerField(default=0)
    date_of_next_payout = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.fullname


def userprofile(signal, **kwargs):
    if kwargs['created']:
        user = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(userprofile, User)
